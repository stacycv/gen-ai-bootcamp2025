//go:build mage
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	_ "github.com/mattn/go-sqlite3"
	"github.com/magefile/mage/sh"
)

const dbName = "words.db"

// InitDB initializes the SQLite database
func InitDB() error {
	if _, err := os.Stat(dbName); err == nil {
		fmt.Printf("Database %s already exists\n", dbName)
		return nil
	}

	db, err := sql.Open("sqlite3", dbName)
	if err != nil {
		return fmt.Errorf("failed to create database: %v", err)
	}
	defer db.Close()

	fmt.Printf("Created database %s\n", dbName)
	return nil
}

// Migrate runs all pending migrations
func Migrate() error {
	db, err := sql.Open("sqlite3", dbName)
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	migrations, err := filepath.Glob("db/migrations/*.sql")
	if err != nil {
		return fmt.Errorf("failed to read migrations: %v", err)
	}

	sort.Strings(migrations)

	for _, migration := range migrations {
		fmt.Printf("Running migration %s\n", migration)
		
		content, err := os.ReadFile(migration)
		if err != nil {
			return fmt.Errorf("failed to read migration %s: %v", migration, err)
		}

		queries := strings.Split(string(content), ";")
		for _, query := range queries {
			query = strings.TrimSpace(query)
			if query == "" {
				continue
			}

			if _, err := db.Exec(query); err != nil {
				return fmt.Errorf("failed to execute migration %s: %v", migration, err)
			}
		}
	}

	return nil
}

// ImportData imports words from JSON files in the seeds directory
func ImportData() error {
	db, err := sql.Open("sqlite3", dbName)
	if err != nil {
		return fmt.Errorf("failed to open database: %v", err)
	}
	defer db.Close()

	files, err := filepath.Glob("db/seeds/*.json")
	if err != nil {
		return fmt.Errorf("failed to read seed files: %v", err)
	}

	for _, file := range files {
		fmt.Printf("Processing seed file: %s\n", file)
		
		content, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read seed file %s: %v", file, err)
		}

		var seedData struct {
			GroupName string `json:"group_name"`
			Words     []struct {
				FormalSpanish   string `json:"formal_spanish"`
				InformalSpanish string `json:"informal_spanish"`
				English         string `json:"english"`
			} `json:"words"`
		}

		if err := json.Unmarshal(content, &seedData); err != nil {
			return fmt.Errorf("failed to parse seed file %s: %v", file, err)
		}

		// Begin transaction
		tx, err := db.Begin()
		if err != nil {
			return fmt.Errorf("failed to start transaction: %v", err)
		}

		// Create group
		result, err := tx.Exec("INSERT INTO groups (name) VALUES (?)", seedData.GroupName)
		if err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to insert group: %v", err)
		}

		groupID, err := result.LastInsertId()
		if err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to get group ID: %v", err)
		}

		// Insert words and create word-group relationships
		for _, word := range seedData.Words {
			result, err := tx.Exec(`
				INSERT INTO words (formal_spanish, informal_spanish, english)
				VALUES (?, ?, ?)`,
				word.FormalSpanish, word.InformalSpanish, word.English,
			)
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to insert word: %v", err)
			}

			wordID, err := result.LastInsertId()
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to get word ID: %v", err)
			}

			_, err = tx.Exec("INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)", wordID, groupID)
			if err != nil {
				tx.Rollback()
				return fmt.Errorf("failed to create word-group relationship: %v", err)
			}
		}

		if err := tx.Commit(); err != nil {
			return fmt.Errorf("failed to commit transaction: %v", err)
		}

		fmt.Printf("Successfully imported group '%s' with %d words\n", seedData.GroupName, len(seedData.Words))
	}

	return nil
}

// Clean removes the database file
func Clean() error {
	return os.Remove(dbName)
}

// Reset runs Clean, InitDB, Migrate, and ImportData in sequence
func Reset() error {
	if err := Clean(); err != nil && !os.IsNotExist(err) {
		return err
	}
	if err := InitDB(); err != nil {
		return err
	}
	if err := Migrate(); err != nil {
		return err
	}
	return ImportData()
} 