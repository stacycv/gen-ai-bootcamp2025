package service

import (
	"database/sql"
	"errors"
	"time"
)

type StudyActivity struct {
	ID           int64  `json:"id"`
	Name         string `json:"name"`
	Description  string `json:"description"`
	ThumbnailURL string `json:"thumbnail_url"`
	LaunchURL    string `json:"launch_url"`
}

type StudyActivitySession struct {
	ID                  int64     `json:"id"`
	ActivityName        string    `json:"activity_name"`
	ActivityDescription string    `json:"activity_description"`
	GroupName          string    `json:"group_name"`
	StartTime          time.Time `json:"start_time"`
	EndTime            time.Time `json:"end_time"`
	WordsReviewed      int       `json:"words_reviewed"`
	SuccessRate        int       `json:"success_rate"`
}

type StudyActivityService struct {
	db *sql.DB
}

func NewStudyActivityService(db *sql.DB) *StudyActivityService {
	return &StudyActivityService{db: db}
}

func (s *StudyActivityService) GetStudyActivity(id int64) (*StudyActivity, error) {
	activity := &StudyActivity{}
	err := s.db.QueryRow(`
		SELECT id, name, description, thumbnail_url, launch_url
		FROM study_activities
		WHERE id = ?`,
		id,
	).Scan(
		&activity.ID,
		&activity.Name,
		&activity.Description,
		&activity.ThumbnailURL,
		&activity.LaunchURL,
	)

	if err == sql.ErrNoRows {
		return nil, errors.New("study activity not found")
	}
	if err != nil {
		return nil, err
	}

	return activity, nil
}

func (s *StudyActivityService) GetStudyActivitySessions(activityID int64, page, perPage int) ([]StudyActivitySession, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow(`
		SELECT COUNT(*) 
		FROM study_sessions 
		WHERE study_activity_id = ?`,
		activityID,
	).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated sessions with details
	rows, err := s.db.Query(`
		SELECT 
			ss.id,
			sa.name as activity_name,
			sa.description as activity_description,
			g.name as group_name,
			ss.created_at as start_time,
			COALESCE(MAX(wri.created_at), ss.created_at) as end_time,
			COUNT(DISTINCT wri.word_id) as words_reviewed,
			CAST(
				SUM(CASE WHEN wri.correct THEN 1 ELSE 0 END) * 100.0 / 
				NULLIF(COUNT(wri.word_id), 0) 
			AS INTEGER) as success_rate
		FROM study_sessions ss
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE ss.study_activity_id = ?
		GROUP BY ss.id, sa.name, sa.description, g.name, ss.created_at
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`,
		activityID, perPage, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var sessions []StudyActivitySession
	for rows.Next() {
		var session StudyActivitySession
		if err := rows.Scan(
			&session.ID,
			&session.ActivityName,
			&session.ActivityDescription,
			&session.GroupName,
			&session.StartTime,
			&session.EndTime,
			&session.WordsReviewed,
			&session.SuccessRate,
		); err != nil {
			return nil, 0, err
		}
		sessions = append(sessions, session)
	}

	return sessions, total, nil
} 