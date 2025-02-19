package service

import "database/sql"

type ResetService struct {
	db *sql.DB
}

func NewResetService(db *sql.DB) *ResetService {
	return &ResetService{db: db}
}

func (s *ResetService) ResetHistory() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	// Delete all study sessions and related data
	_, err = tx.Exec("DELETE FROM word_review_items")
	if err != nil {
		tx.Rollback()
		return err
	}

	_, err = tx.Exec("DELETE FROM study_activities")
	if err != nil {
		tx.Rollback()
		return err
	}

	_, err = tx.Exec("DELETE FROM study_sessions")
	if err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit()
}

func (s *ResetService) FullReset() error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	// Delete all data
	tables := []string{
		"word_review_items",
		"study_activities",
		"study_sessions",
		"word_groups",
		"words",
		"groups",
	}

	for _, table := range tables {
		_, err = tx.Exec("DELETE FROM " + table)
		if err != nil {
			tx.Rollback()
			return err
		}
	}

	return tx.Commit()
} 