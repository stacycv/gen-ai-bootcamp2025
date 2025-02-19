package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"

	"backend_go/internal/service"
)

type StudySessionHandler struct {
	studySessionService *service.StudySessionService
}

func NewStudySessionHandler(studySessionService *service.StudySessionService) *StudySessionHandler {
	return &StudySessionHandler{studySessionService: studySessionService}
}

func (h *StudySessionHandler) GetStudySessions(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	perPage, _ := strconv.Atoi(c.DefaultQuery("per_page", "100"))

	sessions, total, err := h.studySessionService.GetStudySessions(page, perPage)
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

func (h *StudySessionHandler) CreateStudySession(c *gin.Context) {
	var req struct {
		GroupID         int64 `json:"group_id" binding:"required"`
		StudyActivityID int64 `json:"study_activity_id" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	session, err := h.studySessionService.CreateStudySession(req.GroupID, req.StudyActivityID)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "group not found" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, session)
}

func (h *StudySessionHandler) AddWordReview(c *gin.Context) {
	sessionID, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid session ID"})
		return
	}

	wordID, err := strconv.ParseInt(c.Param("word_id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid word ID"})
		return
	}

	var req struct {
		Correct bool `json:"correct" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err = h.studySessionService.AddWordReview(sessionID, wordID, req.Correct)
	if err != nil {
		status := http.StatusInternalServerError
		if err.Error() == "study session not found" || err.Error() == "word not found" {
			status = http.StatusNotFound
		}
		c.JSON(status, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"word_id": wordID,
		"study_session_id": sessionID,
		"correct": req.Correct,
	})
}

func (h *StudySessionHandler) GetSessionWords(c *gin.Context) {
	sessionID, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid session ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	perPage, _ := strconv.Atoi(c.DefaultQuery("per_page", "100"))

	words, total, err := h.studySessionService.GetSessionWords(sessionID, page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	totalPages := (total + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": words,
		"pagination": gin.H{
			"current_page": page,
			"total_pages": totalPages,
			"per_page":    perPage,
		},
	})
} 