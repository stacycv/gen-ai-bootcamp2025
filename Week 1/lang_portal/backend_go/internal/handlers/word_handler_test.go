package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"

	"backend_go/internal/service"
	"backend_go/internal/test"
)

func TestWordHandler_GetWords(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()

	// Load test data
	test.LoadFixtures(t, db, "words")

	// Create handler
	wordService := service.NewWordService(db)
	handler := NewWordHandler(wordService)

	// Create test router
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/words", handler.GetWords)

	// Test cases
	tests := []struct {
		name           string
		query          string
		expectedStatus int
		expectedItems  int
		expectedPages  int
	}{
		{
			name:           "Default pagination",
			query:          "",
			expectedStatus: http.StatusOK,
			expectedItems:  3,
			expectedPages:  1,
		},
		{
			name:           "Custom pagination",
			query:          "?page=1&per_page=2",
			expectedStatus: http.StatusOK,
			expectedItems:  2,
			expectedPages:  2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create request
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/words"+tt.query, nil)
			r.ServeHTTP(w, req)

			// Assert status code
			assert.Equal(t, tt.expectedStatus, w.Code)

			// Parse response
			var response struct {
				Items []struct {
					ID              int64  `json:"id"`
					FormalSpanish   string `json:"formal_spanish"`
					InformalSpanish string `json:"informal_spanish"`
					English         string `json:"english"`
				} `json:"items"`
				Pagination struct {
					CurrentPage int `json:"current_page"`
					TotalPages  int `json:"total_pages"`
					PerPage     int `json:"per_page"`
				} `json:"pagination"`
			}
			err := json.Unmarshal(w.Body.Bytes(), &response)
			assert.NoError(t, err)

			// Assert response structure
			assert.Len(t, response.Items, tt.expectedItems)
			assert.Equal(t, tt.expectedPages, response.Pagination.TotalPages)
		})
	}
} 