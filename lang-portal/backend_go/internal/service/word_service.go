package service

import (
	"database/sql"
	"errors"

	"backend_go/internal/models"
)

type WordService struct {
	db *sql.DB
}

func NewWordService(db *sql.DB) *WordService {
	return &WordService{db: db}
}

func (s *WordService) GetWords(page, perPage int) ([]models.Word, int, error) {
	offset := (page - 1) * perPage

	// Get total count
	var total int
	err := s.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated words
	rows, err := s.db.Query(`
		SELECT id, formal_spanish, informal_spanish, english, parts 
		FROM words 
		LIMIT ? OFFSET ?`,
		perPage, offset,
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

func (s *WordService) GetWordByID(id int64) (*models.Word, error) {
	word := &models.Word{}
	err := s.db.QueryRow(`
		SELECT id, formal_spanish, informal_spanish, english, parts 
		FROM words 
		WHERE id = ?`,
		id,
	).Scan(
		&word.ID,
		&word.FormalSpanish,
		&word.InformalSpanish,
		&word.English,
		&word.Parts,
	)

	if err == sql.ErrNoRows {
		return nil, errors.New("word not found")
	}
	if err != nil {
		return nil, err
	}

	return word, nil
} 