package models

import "time"

type Word struct {
	ID              int64  `json:"id" db:"id"`
	FormalSpanish   string `json:"formal_spanish" db:"formal_spanish"`
	InformalSpanish string `json:"informal_spanish" db:"informal_spanish"`
	English         string `json:"english" db:"english"`
	Parts           string `json:"parts" db:"parts"` // JSON string
}

type Group struct {
	ID        int64  `json:"id" db:"id"`
	Name      string `json:"name" db:"name"`
	WordCount int    `json:"word_count" db:"word_count"`
}

type WordGroup struct {
	ID      int64 `json:"id" db:"id"`
	WordID  int64 `json:"word_id" db:"word_id"`
	GroupID int64 `json:"group_id" db:"group_id"`
}

type StudySession struct {
	ID              int64     `json:"id" db:"id"`
	GroupID         int64     `json:"group_id" db:"group_id"`
	CreatedAt       time.Time `json:"created_at" db:"created_at"`
	StudyActivityID int64     `json:"study_activity_id" db:"study_activity_id"`
}

type StudyActivity struct {
	ID              int64     `json:"id" db:"id"`
	StudySessionID  int64     `json:"study_session_id" db:"study_session_id"`
	GroupID         int64     `json:"group_id" db:"group_id"`
	CreatedAt       time.Time `json:"created_at" db:"created_at"`
}

type WordReviewItem struct {
	WordID         int64     `json:"word_id" db:"word_id"`
	StudySessionID int64     `json:"study_session_id" db:"study_session_id"`
	Correct        bool      `json:"correct" db:"correct"`
	CreatedAt      time.Time `json:"created_at" db:"created_at"`
} 