package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"backend_go/internal/service"
)

type StudyActivityHandler struct {
	studyActivityService *service.StudyActivityService
}

func NewStudyActivityHandler(studyActivityService *service.StudyActivityService) *StudyActivityHandler {
	return &StudyActivityHandler{studyActivityService: studyActivityService}
}

func (h *StudyActivityHandler) GetStudyActivity(c *gin.Context) {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid activity ID"})
		return
	}

	activity, err := h.studyActivityService.GetStudyActivity(id)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "study activity not found" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, activity)
}

func (h *StudyActivityHandler) GetStudyActivitySessions(c *gin.Context) {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid activity ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	perPage, _ := strconv.Atoi(c.DefaultQuery("per_page", "100"))

	sessions, total, err := h.studyActivityService.GetStudyActivitySessions(id, page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	totalPages := (total + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": sessions,
		"pagination": gin.H{
			"current_page": page,
			"total_pages": totalPages,
			"per_page":    perPage,
		},
	})
} 