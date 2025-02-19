package database

import (
	"database/sql"
	"sync"

	_ "github.com/mattn/go-sqlite3"
)

var (
	db   *sql.DB
	once sync.Once
)

// GetDB returns a singleton database connection
func GetDB() (*sql.DB, error) {
	var err error
	once.Do(func() {
		db, err = sql.Open("sqlite3", "words.db")
		if err != nil {
			return
		}

		// Set connection pool settings
		db.SetMaxOpenConns(1) // SQLite only supports one writer at a time
		db.SetMaxIdleConns(1)
	})

	if err != nil {
		return nil, err
	}

	return db, nil
} 