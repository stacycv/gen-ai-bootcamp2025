INSERT INTO study_activities (id, name, description, thumbnail_url, launch_url) VALUES 
(1, 'Flashcards', 'Practice with flashcards', '/thumbnails/flashcards.png', '/activities/flashcards');

INSERT INTO study_sessions (id, group_id, study_activity_id, created_at) VALUES 
(1, 1, 1, CURRENT_TIMESTAMP);

INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES 
(1, 1, true, CURRENT_TIMESTAMP),
(2, 1, false, CURRENT_TIMESTAMP),
(3, 1, true, CURRENT_TIMESTAMP); 