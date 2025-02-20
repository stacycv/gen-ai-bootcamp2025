package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"

	"backend_go/internal/service"
	"backend_go/internal/test"
)

func TestStudySessionHandler_CreateStudySession(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words")

	studySessionService := service.NewStudySessionService(db)
	handler := NewStudySessionHandler(studySessionService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.POST("/api/study-sessions", handler.CreateStudySession)

	tests := []struct {
		name           string
		payload        map[string]interface{}
		expectedStatus int
	}{
		{
			name: "Valid session creation",
			payload: map[string]interface{}{
				"group_id":          1,
				"study_activity_id": 1,
			},
			expectedStatus: http.StatusCreated,
		},
		{
			name: "Invalid group ID",
			payload: map[string]interface{}{
				"group_id":          999,
				"study_activity_id": 1,
			},
			expectedStatus: http.StatusNotFound,
		},
		{
			name: "Missing required fields",
			payload: map[string]interface{}{
				"group_id": 1,
			},
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			payloadBytes, _ := json.Marshal(tt.payload)
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("POST", "/api/study-sessions", bytes.NewBuffer(payloadBytes))
			req.Header.Set("Content-Type", "application/json")
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusCreated {
				var response struct {
					ID              int64 `json:"id"`
					GroupID         int64 `json:"group_id"`
					StudyActivityID int64 `json:"study_activity_id"`
				}
				err := json.Unmarshal(w.Body.Bytes(), &response)
				assert.NoError(t, err)
				assert.NotZero(t, response.ID)
				assert.Equal(t, tt.payload["group_id"], float64(response.GroupID))
			}
		})
	}
}

func TestStudySessionHandler_AddWordReview(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words", "study_sessions")

	studySessionService := service.NewStudySessionService(db)
	handler := NewStudySessionHandler(studySessionService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.POST("/api/study-sessions/:id/words/:word_id/review", handler.AddWordReview)

	tests := []struct {
		name           string
		sessionID      string
		wordID         string
		payload        map[string]interface{}
		expectedStatus int
	}{
		{
			name:      "Valid review",
			sessionID: "1",
			wordID:    "1",
			payload: map[string]interface{}{
				"correct": true,
			},
			expectedStatus: http.StatusOK,
		},
		{
			name:      "Invalid session ID",
			sessionID: "999",
			wordID:    "1",
			payload: map[string]interface{}{
				"correct": true,
			},
			expectedStatus: http.StatusNotFound,
		},
		{
			name:      "Invalid word ID",
			sessionID: "1",
			wordID:    "999",
			payload: map[string]interface{}{
				"correct": true,
			},
			expectedStatus: http.StatusNotFound,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			payloadBytes, _ := json.Marshal(tt.payload)
			w := httptest.NewRecorder()
			req, _ := http.NewRequest(
				"POST",
				"/api/study-sessions/"+tt.sessionID+"/words/"+tt.wordID+"/review",
				bytes.NewBuffer(payloadBytes),
			)
			req.Header.Set("Content-Type", "application/json")
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
				var response struct {
					Success        bool  `json:"success"`
					WordID        int64 `json:"word_id"`
					StudySessionID int64 `json:"study_session_id"`
					Correct       bool  `json:"correct"`
				}
				err := json.Unmarshal(w.Body.Bytes(), &response)
				assert.NoError(t, err)
				assert.True(t, response.Success)
			}
		})
	}
}

func TestStudySessionHandler_GetSessionWords(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words", "study_sessions")

	studySessionService := service.NewStudySessionService(db)
	handler := NewStudySessionHandler(studySessionService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/study-sessions/:id/words", handler.GetSessionWords)

	tests := []struct {
		name           string
		sessionID      string
		query          string
		expectedStatus int
	}{
		{
			name:           "Valid session",
			sessionID:      "1",
			query:          "",
			expectedStatus: http.StatusOK,
		},
		{
			name:           "Invalid session ID",
			sessionID:      "999",
			query:          "",
			expectedStatus: http.StatusNotFound,
		},
		{
			name:           "With pagination",
			sessionID:      "1",
			query:          "?page=1&per_page=2",
			expectedStatus: http.StatusOK,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/study-sessions/"+tt.sessionID+"/words"+tt.query, nil)
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
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
				assert.NotNil(t, response.Items)
			}
		})
	}
} 