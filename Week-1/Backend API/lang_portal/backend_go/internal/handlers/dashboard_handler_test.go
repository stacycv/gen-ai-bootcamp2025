package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"

	"backend_go/internal/service"
	"backend_go/internal/test"
)

func TestDashboardHandler_GetQuickStats(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()

	// Load test data
	test.LoadFixtures(t, db, "words", "study_sessions")

	// Create handler
	dashboardService := service.NewDashboardService(db)
	handler := NewDashboardHandler(dashboardService)

	// Create test router
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/dashboard/quick-stats", handler.GetQuickStats)

	// Make request
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/api/dashboard/quick-stats", nil)
	r.ServeHTTP(w, req)

	// Assert status code
	assert.Equal(t, http.StatusOK, w.Code)

	// Parse response
	var response struct {
		TotalWordsAvailable  int       `json:"total_words_available"`
		TotalGroups          int       `json:"total_groups"`
		TotalStudySessions   int       `json:"total_study_sessions"`
		LastStudySessionDate time.Time `json:"last_study_session_date"`
		OverallAccuracy      int       `json:"overall_accuracy"`
	}
	err := json.Unmarshal(w.Body.Bytes(), &response)
	assert.NoError(t, err)

	// Assert response values
	assert.Equal(t, 3, response.TotalWordsAvailable)
	assert.Equal(t, 1, response.TotalGroups)
	// Add more assertions based on your test data
} 