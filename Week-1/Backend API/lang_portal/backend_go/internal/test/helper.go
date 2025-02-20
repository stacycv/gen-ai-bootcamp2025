package test

import (
	"database/sql"
	"os"
	"testing"

	"backend_go/internal/database"
)

const testDBName = "test.db"

// SetupTestDB creates a test database and returns a cleanup function
func SetupTestDB(t *testing.T) (*sql.DB, func()) {
	// Remove any existing test database
	os.Remove(testDBName)

	// Create test database
	db, err := sql.Open("sqlite3", testDBName)
	if err != nil {
		t.Fatalf("Failed to create test database: %v", err)
	}

	// Run migrations
	if err := runMigrations(db); err != nil {
		t.Fatalf("Failed to run migrations: %v", err)
	}

	// Return cleanup function
	cleanup := func() {
		db.Close()
		os.Remove(testDBName)
	}

	return db, cleanup
}

// Helper to load test fixtures
func LoadFixtures(t *testing.T, db *sql.DB, fixtures ...string) {
	for _, fixture := range fixtures {
		// Load and execute SQL from fixture file
		content, err := os.ReadFile("testdata/fixtures/" + fixture + ".sql")
		if err != nil {
			t.Fatalf("Failed to read fixture %s: %v", fixture, err)
		}

		_, err = db.Exec(string(content))
		if err != nil {
			t.Fatalf("Failed to load fixture %s: %v", fixture, err)
		}
	}
} 