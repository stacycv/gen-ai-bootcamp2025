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

func TestGroupHandler_GetGroups(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()

	// Load test data
	test.LoadFixtures(t, db, "words")

	// Create handler
	groupService := service.NewGroupService(db)
	handler := NewGroupHandler(groupService)

	// Create test router
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/groups", handler.GetGroups)

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
			expectedItems:  1, // From our test fixture
			expectedPages:  1,
		},
		{
			name:           "Custom pagination",
			query:          "?page=1&per_page=1",
			expectedStatus: http.StatusOK,
			expectedItems:  1,
			expectedPages:  1,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/groups"+tt.query, nil)
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			var response struct {
				Items []struct {
					ID        int64  `json:"id"`
					Name      string `json:"name"`
					WordCount int    `json:"word_count"`
				} `json:"items"`
				Pagination struct {
					CurrentPage int `json:"current_page"`
					TotalPages  int `json:"total_pages"`
					PerPage     int `json:"per_page"`
				} `json:"pagination"`
			}
			err := json.Unmarshal(w.Body.Bytes(), &response)
			assert.NoError(t, err)

			assert.Len(t, response.Items, tt.expectedItems)
			assert.Equal(t, tt.expectedPages, response.Pagination.TotalPages)
		})
	}
}

func TestGroupHandler_GetGroupByID(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words")

	groupService := service.NewGroupService(db)
	handler := NewGroupHandler(groupService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/groups/:id", handler.GetGroupByID)

	tests := []struct {
		name           string
		groupID        string
		expectedStatus int
	}{
		{
			name:           "Valid group ID",
			groupID:        "1",
			expectedStatus: http.StatusOK,
		},
		{
			name:           "Invalid group ID",
			groupID:        "999",
			expectedStatus: http.StatusNotFound,
		},
		{
			name:           "Invalid ID format",
			groupID:        "abc",
			expectedStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/groups/"+tt.groupID, nil)
			r.ServeHTTP(w, req)

			assert.Equal(t, tt.expectedStatus, w.Code)

			if tt.expectedStatus == http.StatusOK {
				var response struct {
					ID        int64  `json:"id"`
					Name      string `json:"name"`
					WordCount int    `json:"word_count"`
				}
				err := json.Unmarshal(w.Body.Bytes(), &response)
				assert.NoError(t, err)
				assert.NotEmpty(t, response.Name)
			}
		})
	}
}

func TestGroupHandler_GetGroupWords(t *testing.T) {
	// Setup
	db, cleanup := test.SetupTestDB(t)
	defer cleanup()
	test.LoadFixtures(t, db, "words")

	groupService := service.NewGroupService(db)
	handler := NewGroupHandler(groupService)

	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/api/groups/:id/words", handler.GetGroupWords)

	tests := []struct {
		name           string
		groupID        string
		query          string
		expectedStatus int
		expectedItems  int
	}{
		{
			name:           "Valid group with words",
			groupID:        "1",
			query:          "",
			expectedStatus: http.StatusOK,
			expectedItems:  3, // From our test fixture
		},
		{
			name:           "Invalid group ID",
			groupID:        "999",
			query:          "",
			expectedStatus: http.StatusNotFound,
			expectedItems:  0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			w := httptest.NewRecorder()
			req, _ := http.NewRequest("GET", "/api/groups/"+tt.groupID+"/words"+tt.query, nil)
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
				assert.Len(t, response.Items, tt.expectedItems)
			}
		})
	}
} 