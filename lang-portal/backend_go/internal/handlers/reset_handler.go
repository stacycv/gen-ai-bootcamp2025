package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"backend_go/internal/service"
)

type ResetHandler struct {
	resetService *service.ResetService
}

func NewResetHandler(resetService *service.ResetService) *ResetHandler {
	return &ResetHandler{resetService: resetService}
}

func (h *ResetHandler) ResetHistory(c *gin.Context) {
	if err := h.resetService.ResetHistory(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Study history has been reset",
	})
}

func (h *ResetHandler) FullReset(c *gin.Context) {
	if err := h.resetService.FullReset(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "All data has been reset",
	})
} 