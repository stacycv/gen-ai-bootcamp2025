import random

class Exercise:
    def __init__(self):
        self.exercises = {
            "basics": [
                {
                    "type": "multiple_choice",
                    "question": "How do you say 'Hello' in Spanish?",
                    "options": ["Hola", "Adiós", "Gracias", "Por favor"],
                    "correct": "Hola",
                    "audio": "hello.mp3"
                },
                {
                    "type": "translation",
                    "question": "Translate: Good morning",
                    "correct": "Buenos días",
                    "audio": "good_morning.mp3"
                },
                {
                    "type": "matching",
                    "pairs": [
                        ("Hello", "Hola"),
                        ("Goodbye", "Adiós"),
                        ("Thank you", "Gracias"),
                        ("Please", "Por favor")
                    ]
                }
            ],
            "family": [
                {
                    "type": "multiple_choice",
                    "question": "How do you say 'Mother' in Spanish?",
                    "options": ["Madre", "Padre", "Hermana", "Tía"],
                    "correct": "Madre",
                    "audio": "mother.mp3"
                }
            ],
            "food": [
                {
                    "type": "multiple_choice",
                    "question": "How do you say 'Water' in Spanish?",
                    "options": ["Agua", "Pan", "Leche", "Café"],
                    "correct": "Agua",
                    "audio": "water.mp3"
                }
            ]
        }
    
    def get_exercise(self, category):
        return random.choice(self.exercises.get(category, self.exercises["basics"])) 