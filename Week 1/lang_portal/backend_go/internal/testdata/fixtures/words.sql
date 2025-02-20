INSERT INTO words (formal_spanish, informal_spanish, english) VALUES
('usted come', 'tú comes', 'you eat'),
('usted habla', 'tú hablas', 'you speak'),
('usted vive', 'tú vives', 'you live');

INSERT INTO groups (name) VALUES ('Basic Verbs');

INSERT INTO word_groups (word_id, group_id) VALUES (1, 1), (2, 1), (3, 1); 