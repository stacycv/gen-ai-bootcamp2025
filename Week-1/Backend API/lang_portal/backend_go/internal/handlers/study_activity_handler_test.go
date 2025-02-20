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

func TestStudyActivityHandler_GetStudyActivity(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words", "study_sessions")

	studyActivityService := service.NewStudyActivityService(db)
	handler := NewStudyActivityHandler(studyActivityService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/study-activities/:id", handler.GetStudyActivity)

	tests := []struct {
		name           string
		activityID     string
		expectedStatus int
	}{
		{
			name:           "Valid activity ID",
			activityID:     "1",
			expectedStatus: http.StatusOK,
		},
		{
			name:           "Invalid activity ID",
			activityID:     "999",
			expectedStatus: http.StatusNotFound,
		},
		{
			name:           "Invalid ID format",
			activityID:     "abc",
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/study-activities/"+tt.activityID, nil)
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
				var response struct {
					ID           int64  `json:"id"`
					Name         string `json:"name"`
					Description  string `json:"description"`
					ThumbnailURL string `json:"thumbnail_url"`
					LaunchURL    string `json:"launch_url"`
				}
				err := json.Unmarshal(w.Body.Bytes(), &response)
				assert.NoError(t, err)
				assert.Equal(t, "Flashcards", response.Name)
			}
		})
	}
}

func TestStudyActivityHandler_GetStudyActivitySessions(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words", "study_sessions")

	studyActivityService := service.NewStudyActivityService(db)
	handler := NewStudyActivityHandler(studyActivityService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/study-activities/:id/study-sessions", handler.GetStudyActivitySessions)

	tests := []struct {
		name           string
		activityID     string
		query          string
		expectedStatus int
	}{
		{
			name:           "Valid activity with sessions",
			activityID:     "1",
			query:          "",
			expectedStatus: http.StatusOK,
		},
		{
			name:           "Invalid activity ID",
			activityID:     "999",
			query:          "",
			expectedStatus: http.StatusNotFound,
		},
		{
			name:           "With pagination",
			activityID:     "1",
			query:          "?page=1&per_page=2",
			expectedStatus: http.StatusOK,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/study-activities/"+tt.activityID+"/study-sessions"+tt.query, nil)
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
				var response struct {
					Items []struct {
						ID                  int64  `json:"id"`
						ActivityName        string `json:"activity_name"`
						ActivityDescription string `json:"activity_description"`
						GroupName          string `json:"group_name"`
						WordsReviewed      int    `json:"words_reviewed"`
						SuccessRate        int    `json:"success_rate"`
					} `json:"items"`
					Pagination struct {
						CurrentPage int `json:"current_page"`
						TotalPages  int `json:"total_pages"`
						PerPage     int `json:"per_page"`
					} `json:"pagination"`
				}
				err := json.Unmarshal(w.Body.Bytes(), &response)
				assert.NoError(t, err)
				assert.NotNil(t, response.Items)

				if len(response.Items) > 0 {
					assert.Equal(t, "Flashcards", response.Items[0].ActivityName)
					assert.Equal(t, "Practice with flashcards", response.Items[0].ActivityDescription)
				}
			}
		})
	}
} 