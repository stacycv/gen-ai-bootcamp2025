package service

import (
	"database/sql"
	"errors"
	"time"

	"backend_go/internal/models"
)

type StudySessionService struct {
	db *sql.DB
}

func NewStudySessionService(db *sql.DB) *StudySessionService {
	return &StudySessionService{db: db}
}

func (s *StudySessionService) GetStudySessions(page, perPage int) ([]models.StudySession, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow("SELECT COUNT(*) FROM study_sessions").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated study sessions with additional info
	rows, err := s.db.Query(`
		SELECT 
			ss.id, 
			ss.group_id,
			g.name as group_name,
			ss.created_at,
			ss.study_activity_id,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		GROUP BY ss.id, ss.group_id, g.name, ss.created_at, ss.study_activity_id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`,
		perPage, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var sessions []models.StudySession
	for rows.Next() {
		var session models.StudySession
		var groupName string
		var reviewItemsCount int
		if err := rows.Scan(
			&session.ID,
			&session.GroupID,
			&groupName,
			&session.CreatedAt,
			&session.StudyActivityID,
			&reviewItemsCount,
		); err != nil {
			return nil, 0, err
		}
		sessions = append(sessions, session)
	}

	return sessions, total, nil
}

func (s *StudySessionService) CreateStudySession(groupID, studyActivityID int64) (*models.StudySession, error) {
	// Verify group exists
	var exists bool
	err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?)", groupID).Scan(&exists)
	if err != nil {
		return nil, err
	}
	if !exists {
		return nil, errors.New("group not found")
	}

	// Create study session
	result, err := s.db.Exec(`
		INSERT INTO study_sessions (group_id, study_activity_id, created_at)
		VALUES (?, ?, ?)`,
		groupID, studyActivityID, time.Now(),
	)
	if err != nil {
		return nil, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}

	session := &models.StudySession{
		ID:              id,
		GroupID:         groupID,
		StudyActivityID: studyActivityID,
		CreatedAt:       time.Now(),
	}

	return session, nil
}

func (s *StudySessionService) AddWordReview(sessionID, wordID int64, correct bool) error {
	// Verify session exists
	var exists bool
	err := s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM study_sessions WHERE id = ?)", sessionID).Scan(&exists)
	if err != nil {
		return err
	}
	if !exists {
		return errors.New("study session not found")
	}

	// Verify word exists
	err = s.db.QueryRow("SELECT EXISTS(SELECT 1 FROM words WHERE id = ?)", wordID).Scan(&exists)
	if err != nil {
		return err
	}
	if !exists {
		return errors.New("word not found")
	}

	// Add word review
	_, err = s.db.Exec(`
		INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
		VALUES (?, ?, ?, ?)`,
		wordID, sessionID, correct, time.Now(),
	)
	return err
}

func (s *StudySessionService) GetSessionWords(sessionID int64, page, perPage int) ([]models.Word, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow(`
		SELECT COUNT(DISTINCT w.id)
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?`,
		sessionID,
	).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated words with review status
	rows, err := s.db.Query(`
		SELECT DISTINCT
			w.id,
			w.formal_spanish,
			w.informal_spanish,
			w.english,
			w.parts,
			wri.correct
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?
		LIMIT ? OFFSET ?`,
		sessionID, perPage, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var words []models.Word
	for rows.Next() {
		var word models.Word
		var correct bool
		if err := rows.Scan(
			&word.ID,
			&word.FormalSpanish,
			&word.InformalSpanish,
			&word.English,
			&word.Parts,
			&correct,
		); err != nil {
			return nil, 0, err
		}
		words = append(words, word)
	}

	return words, total, nil
} 