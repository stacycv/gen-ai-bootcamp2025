package service

import (
	"database/sql"
	"errors"

	"backend_go/internal/models"
)

type GroupService struct {
	db *sql.DB
}

func NewGroupService(db *sql.DB) *GroupService {
	return &GroupService{db: db}
}

func (s *GroupService) GetGroups(page, perPage int) ([]models.Group, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated groups with word count
	rows, err := s.db.Query(`
		SELECT g.id, g.name, COUNT(wg.word_id) as word_count
		FROM groups g
		LEFT JOIN word_groups wg ON g.id = wg.group_id
		GROUP BY g.id, g.name
		LIMIT ? OFFSET ?`,
		perPage, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var groups []models.Group
	for rows.Next() {
		var group models.Group
		var wordCount int
		if err := rows.Scan(&group.ID, &group.Name, &wordCount); err != nil {
			return nil, 0, err
		}
		group.WordCount = wordCount
		groups = append(groups, group)
	}

	return groups, total, nil
}

func (s *GroupService) GetGroupByID(id int64) (*models.Group, error) {
	group := &models.Group{}
	
	// Get group info and word count
	err := s.db.QueryRow(`
		SELECT g.id, g.name, COUNT(wg.word_id) as word_count
		FROM groups g
		LEFT JOIN word_groups wg ON g.id = wg.group_id
		WHERE g.id = ?
		GROUP BY g.id, g.name`,
		id,
	).Scan(&group.ID, &group.Name, &group.WordCount)

	if err == sql.ErrNoRows {
		return nil, errors.New("group not found")
	}
	if err != nil {
		return nil, err
	}

	return group, nil
}

func (s *GroupService) GetGroupWords(groupID int64, page, perPage int) ([]models.Word, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow(`
		SELECT COUNT(*) 
		FROM word_groups wg
		WHERE wg.group_id = ?`,
		groupID,
	).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated words for group
	rows, err := s.db.Query(`
		SELECT w.id, w.formal_spanish, w.informal_spanish, w.english, w.parts
		FROM words w
		JOIN word_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?
		LIMIT ? OFFSET ?`,
		groupID, perPage, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var words []models.Word
	for rows.Next() {
		var word models.Word
		if err := rows.Scan(
			&word.ID,
			&word.FormalSpanish,
			&word.InformalSpanish,
			&word.English,
			&word.Parts,
		); err != nil {
			return nil, 0, err
		}
		words = append(words, word)
	}

	return words, total, nil
}

func (s *GroupService) GetGroupStudySessions(groupID int64, page, perPage int) ([]StudyActivitySession, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow(`
		SELECT COUNT(*) 
		FROM study_sessions 
		WHERE group_id = ?`,
		groupID,
	).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated sessions
	rows, err := s.db.Query(`
		SELECT 
			ss.id,
			sa.name as activity_name,
			ss.created_at as start_time,
			COALESCE(MAX(wri.created_at), ss.created_at) as end_time,
			COUNT(DISTINCT wri.word_id) as review_items_count
		FROM study_sessions ss
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE ss.group_id = ?
		GROUP BY ss.id, sa.name, ss.created_at
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`,
		groupID, perPage, offset,
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
			&session.StartTime,
			&session.EndTime,
			&session.WordsReviewed,
		); err != nil {
			return nil, 0, err
		}
		sessions = append(sessions, session)
	}

	return sessions, total, nil
} 