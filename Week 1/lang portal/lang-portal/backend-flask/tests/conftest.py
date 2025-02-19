import pytest
import sqlite3
from app import create_app

@pytest.fixture(scope='function')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    # Set up test database
    db = sqlite3.connect(':memory:', check_same_thread=False)
    db.row_factory = sqlite3.Row
    app.db = db
    
    # Create tables
    cursor = app.db.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS study_activities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY,
            group_id INTEGER NOT NULL,
            study_activity_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
        );
        
        -- Insert test data
        INSERT INTO groups (id, name) VALUES (1, 'Test Group');
        INSERT INTO study_activities (id, name) VALUES (1, 'Test Activity');
    ''')
    app.db.commit()
    
    yield app
    
    # Clean up - close the database connection
    db.close()

@pytest.fixture
def client(app):
    return app.test_client() 