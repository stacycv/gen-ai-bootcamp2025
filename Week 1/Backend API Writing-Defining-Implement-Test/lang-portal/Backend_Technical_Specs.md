# Technical Specs

## Business Goal

A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

## Technical Requirements

- The backend should be built using Go.
- The database should will be SQLite3.
- The API will be built using Gin
- The API will always return JSON.
- There will be no authentication or authorization. 
- Everything will be public and treated as a single user.

## Database Schema

Our database will be a SQLite database called `words.db`
That will be located in the root of the project folder of `backend_go`

We have the following tables in the database:

- words - stores all words that can be learned
    - id - integer primary key
    - Formal Spanish  - string
    - Informal Spanish - string
    - English - string
    - parts - json
- word_groups  - join table for wods and groups (many-to-many)
    - id - integer
    - word_id - integer
    - group_id - integer
- groups - thematic groups of words
    - id - integer primary key
    - name - string
- study_sessions - records of study sessions grouping word_review_items
    - id - integer 
    - group_id - integer
    - created_at - timestamp     
    - study_activity_id - integer
- study_activities - a specific instance of a study session, linking a study_session to a group
    - id - integer
    - study_session_id - integer
    - group_id - integer
    - created_at - timestamp
- word_review_items - a record of word practice, determining if the word was answered correctly or incorrectly
    - word_id - integer
    - study_session_id - integer
    - correct - boolean
    - created_at - timestamp 

## API Endpoint

### GET /api/dashboard/last-study-session
Returns information about the most recent study session.
#### JSON Response
```json
{
    "id": 123,
    "group_id": 456,
    "created_at": "2024-03-20T15:30:00Z",
    "study_activity_id": 789,
    "group_id": 456
    "group_name": "Basic Greetings"
}
```


### GET /api/dashboard/study-progress
Returns statistics about the study progress.
Please know that the frontend will deterrmine progress bar based on total words studied and total avaliable words.
#### JSON Response
```json
{
"total_words_studied": 4,
"total_avaliable_words": 102,
}
```

### GET /api/dashboard/quick-stats
Returns quick overviewstats about the study progress.
#### JSON Response
```json
{
"total_words_available": 1000,
"total_groups": 20,
"total_study_sessions": 50,
"last_study_session_date": "2024-03-20T15:30:00Z",
"overall_accuracy": 75
}
```

### GET /api/study-activities/:id
Returns information about a specific study activity.
#### JSON Response
```json
{
  "id": 1,
  "name": "Flashcards",
  "description": "Practice with flashcards",
  "thumbnail_url": "path/to/thumbnail.jpg",
  "launch_url": "https://..."
}
```

### GET /api/study-activities/:id/study-sessions
Returns a list of study sessions for a specific study activity.
    - pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Flashcards",
      "activity_description": "Practice with flashcards",
      "group_name": "Common Verbs",
      "start_time": "2024-03-20T15:30:00Z",
      "end_time": "2024-03-20T15:45:00Z",
      "words_reviewed": 20,
      "success_rate": 75
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### POST /api/study-activities/
Creates a new study activity.
#### Required Params
- group_id integer
- study_activity_id integer

#### JSON Response
```json
{
  "group_id": 1,
  "group_id": 123
}
```

### GET /api/words
    - pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "formal_spanish": "usted come",
      "informal_spanish": "tú comes",
      "english": "you eat",
      "correct_count": 10,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### GET /api/words/:id
Returns information about a specific word.
#### JSON Response
```json
{
  "id": 1,
  "formal_spanish": "usted come",
  "informal_spanish": "tú comes",
  "english": "you eat",
  "stats": {
    "correct_count": 10,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Common Verbs"
    }
  ]
}
```

### GET /api/groups
    - pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Common Verbs",
      "word_count": 50
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### GET /api/groups/:id
Returns information about a specific group.
#### JSON Response
```json
{
  "id": 1,
  "name": "Common Verbs",
  "stats": {
    "total_word_count": 50
  }
}
```

### GET /api/groups/:id/words
Returns a list of words for a specific group.
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "formal_spanish": "usted come",
      "informal_spanish": "tú comes",
      "english": "you eat",
      "correct_count": 10,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### GET /api/groups/:id/study-sessions
Returns a list of study sessions for a specific group.
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Flashcards",
      "start_time": "2024-03-20 15:30:00",
      "end_time": "2024-03-20 15:45:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```
### GET /api/study-sessions
    - pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Flashcards",
      "group_name": "Common Verbs",
      "start_time": "2024-03-20 15:30:00",
      "end_time": "2024-03-20 15:45:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### GET /api/study-sessions/:id
Returns information about a specific study session.
#### JSON Response
```json
{
  "id": 1,
  "activity_name": "Flashcards",
  "group_name": "Common Verbs",
  "start_time": "2024-03-20 15:30:00",
  "end_time": "2024-03-20 15:45:00",
  "review_items_count": 20,
}
```
### GET /api/study-sessions/:id/words
Returns a list of words for a specific study session.
#### JSON Response
```json
{
  "items": [
    {
      "formal_spanish": "usted come",
      "informal_spanish": "tú comes",
      "english": "you eat",
      "correct_count": 10,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "per_page": 100
  }
}
```

### POST /api/reset-history
#### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```

### POST /api/full-reset
#### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```

### POST /api/study-sessions/:id/words/:word_id/review
#### Request Params
- id (study_session_id) integer
- word_id integer
- correct boolean
#### Request Payload
```json
{
  "correct": true,
}
```
#### JSON Response
```json
{
  "success": true,
  "word_id": 1,
  "study_session_id": 1,
  "correct": true,
  "created_at": "2024-03-20 15:30:00"
}
```
## Mage Tasks
Mage is a task runner for Go.
Lets lits out the tasks we need to run our language learning portal.
### Initialize Database
This task will initialize the SQLite database called `words.db`

### Migrate Database
This task will run a series of migrations sql files on the database

Migrations will live in the `migrations` folder.
The migration files will be run in order of their file name.
The file name should look like this:
```SQL
0001_initial_migration.sql
0002_create_words_table.sql
```

### Seed Data
This task will import JSON files and transform them into target data for our database.

All seed files live in the `seeds` folder.
In our task we should have a DSL to specify each seed file and its expected group word name
```json
{
  "spanish_formal": "pagar",
  "spanish_informal": "pagar",
  "english": "to pay",
}
```

### Import Data
This task will import the data into the database.

