package service

import (
	"database/sql"
	"time"
)

type DashboardService struct {
	db *sql.DB
}

type LastStudySession struct {
	ID              int64     `json:"id"`
	GroupID         int64     `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int64     `json:"study_activity_id"`
	GroupName       string    `json:"group_name"`
}

type StudyProgress struct {
	TotalWordsStudied    int `json:"total_words_studied"`
	TotalAvailableWords int `json:"total_available_words"`
}

type QuickStats struct {
	TotalWordsAvailable  int       `json:"total_words_available"`
	TotalGroups          int       `json:"total_groups"`
	TotalStudySessions   int       `json:"total_study_sessions"`
	LastStudySessionDate time.Time `json:"last_study_session_date"`
	OverallAccuracy      int       `json:"overall_accuracy"`
}

func NewDashboardService(db *sql.DB) *DashboardService {
	return &DashboardService{db: db}
}

func (s *DashboardService) GetLastStudySession() (*LastStudySession, error) {
	var session LastStudySession
	err := s.db.QueryRow(`
		SELECT 
			ss.id,
			ss.group_id,
			ss.created_at,
			ss.study_activity_id,
			g.name as group_name
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		ORDER BY ss.created_at DESC
		LIMIT 1
	`).Scan(
		&session.ID,
		&session.GroupID,
		&session.CreatedAt,
		&session.StudyActivityID,
		&session.GroupName,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &session, nil
}

func (s *DashboardService) GetStudyProgress() (*StudyProgress, error) {
	var progress StudyProgress

	// Get total available words
	err := s.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&progress.TotalAvailableWords)
	if err != nil {
		return nil, err
	}

	// Get total words studied (distinct words that have been reviewed)
	err = s.db.QueryRow(`
		SELECT COUNT(DISTINCT word_id) 
		FROM word_review_items
	`).Scan(&progress.TotalWordsStudied)
	if err != nil {
		return nil, err
	}

	return &progress, nil
}

func (s *DashboardService) GetQuickStats() (*QuickStats, error) {
	var stats QuickStats

	// Get total words
	err := s.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&stats.TotalWordsAvailable)
	if err != nil {
		return nil, err
	}

	// Get total groups
	err = s.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&stats.TotalGroups)
	if err != nil {
		return nil, err
	}

	// Get total study sessions
	err = s.db.QueryRow("SELECT COUNT(*) FROM study_sessions").Scan(&stats.TotalStudySessions)
	if err != nil {
		return nil, err
	}

	// Get last study session date
	err = s.db.QueryRow(`
		SELECT created_at 
		FROM study_sessions 
		ORDER BY created_at DESC 
		LIMIT 1
	`).Scan(&stats.LastStudySessionDate)
	if err == sql.ErrNoRows {
		stats.LastStudySessionDate = time.Time{}
	} else if err != nil {
		return nil, err
	}

	// Calculate overall accuracy
	err = s.db.QueryRow(`
		SELECT CAST(
			(SELECT COUNT(*) FROM word_review_items WHERE correct = 1) * 100.0 / 
			NULLIF((SELECT COUNT(*) FROM word_review_items), 0) 
		AS INTEGER)
	`).Scan(&stats.OverallAccuracy)
	if err == sql.ErrNoRows {
		stats.OverallAccuracy = 0
	} else if err != nil {
		return nil, err
	}

	return &stats, nil
} 