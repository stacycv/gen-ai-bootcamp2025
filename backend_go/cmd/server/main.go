package main

import (
	"log"

	"github.com/gin-gonic/gin"

	"backend_go/internal/database"
	"backend_go/internal/handlers"
	"backend_go/internal/service"
)

func main() {
	// Initialize database connection
	db, err := database.GetDB()
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	// Initialize services
	wordService := service.NewWordService(db)
	groupService := service.NewGroupService(db)
	studySessionService := service.NewStudySessionService(db)
	dashboardService := service.NewDashboardService(db)
	resetService := service.NewResetService(db)
	studyActivityService := service.NewStudyActivityService(db)

	// Initialize handlers
	wordHandler := handlers.NewWordHandler(wordService)
	groupHandler := handlers.NewGroupHandler(groupService)
	studySessionHandler := handlers.NewStudySessionHandler(studySessionService)
	dashboardHandler := handlers.NewDashboardHandler(dashboardService)
	resetHandler := handlers.NewResetHandler(resetService)
	studyActivityHandler := handlers.NewStudyActivityHandler(studyActivityService)

	r := gin.Default()

	// Add CORS middleware
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		
		c.Next()
	})

	// API routes
	api := r.Group("/api")
	{
		api.GET("/health", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"status": "ok",
			})
		})

		// Word routes
		api.GET("/words", wordHandler.GetWords)
		api.GET("/words/:id", wordHandler.GetWordByID)

		// Group routes
		api.GET("/groups", groupHandler.GetGroups)
		api.GET("/groups/:id", groupHandler.GetGroupByID)
		api.GET("/groups/:id/words", groupHandler.GetGroupWords)

		// Study Session routes
		api.GET("/study-sessions", studySessionHandler.GetStudySessions)
		api.POST("/study-sessions", studySessionHandler.CreateStudySession)
		api.GET("/study-sessions/:id/words", studySessionHandler.GetSessionWords)
		api.POST("/study-sessions/:id/words/:word_id/review", studySessionHandler.AddWordReview)

		// Dashboard routes
		api.GET("/dashboard/last-study-session", dashboardHandler.GetLastStudySession)
		api.GET("/dashboard/study-progress", dashboardHandler.GetStudyProgress)
		api.GET("/dashboard/quick-stats", dashboardHandler.GetQuickStats)

		// Reset routes
		api.POST("/reset-history", resetHandler.ResetHistory)
		api.POST("/full-reset", resetHandler.FullReset)

		// Study Activity routes
		api.GET("/study-activities/:id", studyActivityHandler.GetStudyActivity)
		api.GET("/study-activities/:id/study-sessions", studyActivityHandler.GetStudyActivitySessions)

		// Add to group routes
		api.GET("/groups/:id/study-sessions", groupHandler.GetGroupStudySessions)
	}

	if err := r.Run(":8080"); err != nil {
		log.Fatal("Failed to start server:", err)
	}
} 