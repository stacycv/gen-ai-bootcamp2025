import streamlit as st
import random
from datetime import datetime
import string

# Configure page settings
st.set_page_config(
    page_title="¡Aprende Español! 🇪🇸",
    page_icon="🇪🇸",
    layout="wide"
)

# Spanish-themed modern educational CSS
st.markdown("""
    <style>
    /* Spanish flag-inspired color palette */
    :root {
        --spain-red: #FF0000;
        --spain-yellow: #FFC400;
        --spain-dark-red: #C60001;
        --neutral-light: #F8F9FA;
        --neutral-dark: #2C3E50;
        --accent-blue: #4A90E2;
    }

    /* Vibrant background with Spanish-inspired pattern */
    .main {
        background: #FFF6E6;
        background-image: 
            linear-gradient(120deg, rgba(255, 196, 0, 0.1) 0%, rgba(255, 0, 0, 0.1) 100%),
            repeating-linear-gradient(45deg, 
                rgba(255, 196, 0, 0.05) 0px, 
                rgba(255, 196, 0, 0.05) 2px,
                transparent 2px, 
                transparent 10px
            );
        background-attachment: fixed;
        color: var(--neutral-dark);
        font-family: 'Helvetica Neue', sans-serif;
        min-height: 100vh;
        position: relative;
    }

    /* Add a subtle border inspired by Spanish tiles */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, 
            var(--spain-red) 0%, 
            var(--spain-yellow) 50%, 
            var(--spain-red) 100%
        );
    }

    /* Modern educational headers */
    h1 {
        color: var(--spain-dark-red);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid var(--spain-yellow);
        padding-bottom: 0.5rem;
    }

    h2, h3 {
        color: var(--neutral-dark);
        font-weight: 600;
    }

    /* Clean, modern buttons */
    .stButton>button {
        background-color: var(--spain-red);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: var(--spain-dark-red);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Educational cards */
    .lesson-card {
        background-color: white;
        border-left: 4px solid var(--spain-red);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Progress indicators */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--spain-red), var(--spain-yellow));
        border-radius: 10px;
    }

    /* Metrics in sidebar */
    .sidebar .stMetric {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        border-left: 3px solid var(--spain-yellow);
        margin: 0.5rem 0;
    }

    /* Chat messages */
    .stChatMessage {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: #28A745;
        color: white;
        border-radius: 8px;
        padding: 0.75rem;
    }

    .stError {
        background-color: var(--spain-red);
        color: white;
        border-radius: 8px;
        padding: 0.75rem;
    }

    /* Info messages */
    .stInfo {
        background-color: var(--spain-yellow);
        color: var(--neutral-dark);
        border-radius: 8px;
        padding: 0.75rem;
    }

    /* Radio buttons */
    .stRadio > label {
        color: var(--neutral-dark) !important;
        font-weight: 500;
    }

    /* Text inputs */
    .stTextInput > div > div > input {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 0.75rem;
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: white;
        border-left: 3px solid var(--spain-red);
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 500;
    }

    /* Sidebar styling */
    .sidebar {
        background-color: var(--neutral-light);
        border-right: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = set()
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = []
if 'shuffled_words' not in st.session_state:
    st.session_state.shuffled_words = None
if 'previous_lesson' not in st.session_state:
    st.session_state.previous_lesson = None
if 'lesson_history' not in st.session_state:
    st.session_state.lesson_history = []
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = {}
if 'placement_test_active' not in st.session_state:
    st.session_state.placement_test_active = False
if 'placement_test_score' not in st.session_state:
    st.session_state.placement_test_score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'lesson_type' not in st.session_state:
    st.session_state.lesson_type = None

# Sample lesson data
lessons = {
    "beginner": {
        "translation": [
            {
                "id": "beg-trans-1",
                "type": "translation",
                "title": "Basic Greetings",
                "content": {
                    "english": "Hello, my name is John.",
                    "spanish": "Hola, mi nombre es John.",
                    "words": ["Hola", "mi", "nombre", "es", "John"]
                }
            },
            # Add more translation exercises...
        ],
        "multiple_choice": [
            {
                "id": "beg-mc-1",
                "type": "multiple_choice",
                "title": "Basic Vocabulary",
                "questions": [
                    {
                        "question": "What is 'apple' in Spanish?",
                        "options": ["manzana", "naranja", "plátano", "pera"],
                        "correct": 0
                    },
                    {
                        "question": "Which means 'good morning'?",
                        "options": ["buenas noches", "buenos días", "buenas tardes", "adiós"],
                        "correct": 1
                    }
                ]
            }
        ],
        "fill_blank": [
            {
                "id": "beg-fb-1",
                "type": "fill_blank",
                "title": "Basic Verbs",
                "sentences": [
                    {
                        "sentence": "Yo ___ un estudiante (ser)",
                        "correct": "soy",
                        "hint": "First person singular of 'ser'"
                    },
                    {
                        "sentence": "Ella ___ en Madrid (vivir)",
                        "correct": "vive",
                        "hint": "Third person singular of 'vivir'"
                    }
                ]
            }
        ],
        "conversation": [
            {
                "id": "beg-conv-1",
                "type": "conversation",
                "title": "At the Café",
                "dialogue": [
                    {
                        "speaker": "Waiter",
                        "text": "¡Buenos días! ¿Qué desea?",
                        "translation": "Good morning! What would you like?"
                    },
                    {
                        "speaker": "You",
                        "options": [
                            "Un café, por favor",
                            "Quiero un té",
                            "Nada, gracias"
                        ],
                        "translations": [
                            "A coffee, please",
                            "I want a tea",
                            "Nothing, thank you"
                        ]
                    }
                ]
            }
        ],
        "audio_practice": [
            {
                "id": "beg-audio-1",
                "type": "audio",
                "title": "Basic Pronunciation",
                "audio_url": "https://example.com/audio/basic_pronunciation.mp3",  # You'll need to host audio files
                "exercises": [
                    {
                        "word": "perro",
                        "translation": "dog",
                        "pronunciation": "peh-rro"
                    },
                    {
                        "word": "casa",
                        "translation": "house",
                        "pronunciation": "kah-sah"
                    }
                ]
            }
        ],
        "song_lessons": [
            {
                "id": "beg-song-1",
                "type": "song",
                "title": "Colors and Numbers Song",
                "video_url": "https://www.youtube.com/embed/DsRKoZGaoEM",  # Spanish Colors Song
                "lyrics": [
                    {
                        "spanish": "Los colores, los colores",
                        "english": "The colors, the colors"
                    },
                    {
                        "spanish": "Rojo, azul y verde",
                        "english": "Red, blue and green"
                    }
                ],
                "exercises": [
                    {
                        "question": "What does 'rojo' mean?",
                        "answer": "red"
                    }
                ]
            }
        ],
        "picture_vocabulary": [
            {
                "id": "beg-pic-1",
                "type": "picture",
                "title": "Basic Spanish Animals",
                "video_url": "https://www.youtube.com/embed/YwYwM1FLYXY",  # Spanish Animals for Beginners
                "exercises": [
                    {
                        "question": "How do you say 'dog' in Spanish?",
                        "options": ["perro", "gato", "pájaro", "pez"],
                        "correct": 0
                    },
                    {
                        "question": "What is 'cat' in Spanish?",
                        "options": ["pájaro", "gato", "perro", "conejo"],
                        "correct": 1
                    }
                ]
            },
            {
                "id": "beg-pic-2",
                "type": "picture",
                "title": "Colors in Spanish",
                "video_url": "https://www.youtube.com/embed/zpLQSdu4V94",  # Spanish Colors
                "exercises": [
                    {
                        "question": "What is 'red' in Spanish?",
                        "options": ["rojo", "azul", "verde", "amarillo"],
                        "correct": 0
                    },
                    {
                        "question": "How do you say 'blue'?",
                        "options": ["verde", "amarillo", "azul", "rojo"],
                        "correct": 2
                    }
                ]
            }
        ],
        "interactive_stories": [
            {
                "id": "beg-story-1",
                "type": "story",
                "title": "A Day in Madrid",
                "content": {}  # The content is now handled within the show_interactive_story function
            }
        ]
    },
    "intermediate": {
        "translation": [
            {
                "id": "int-trans-1",
                "type": "translation",
                "title": "Past Tense",
                "content": {
                    "english": "I went to the store yesterday.",
                    "spanish": "Yo fui a la tienda ayer.",
                    "words": ["Yo", "fui", "a", "la", "tienda", "ayer"]
                }
            }
        ],
        "multiple_choice": [
            {
                "id": "int-mc-1",
                "type": "multiple_choice",
                "title": "Weather and Time",
                "questions": [
                    {
                        "question": "How do you say 'It will rain'?",
                        "options": ["Llueve", "Lloverá", "Llovió", "Lloviendo"],
                        "correct": 1
                    }
                ]
            }
        ],
        "fill_blank": [
            {
                "id": "int-fb-1",
                "type": "fill_blank",
                "title": "Past Tense Practice",
                "sentences": [
                    {
                        "sentence": "Ayer yo ___ al supermercado (ir)",
                        "correct": "fui",
                        "hint": "Past tense of 'ir'"
                    }
                ]
            }
        ],
        "conversation": [
            {
                "id": "int-conv-1",
                "type": "conversation",
                "title": "At the Restaurant",
                "dialogue": [
                    {
                        "speaker": "Waiter",
                        "text": "¿Qué le gustaría ordenar?",
                        "translation": "What would you like to order?"
                    },
                    {
                        "speaker": "You",
                        "options": [
                            "Me gustaría la sopa, por favor",
                            "Quiero el pescado",
                            "El pollo, por favor"
                        ],
                        "translations": [
                            "I would like the soup, please",
                            "I want the fish",
                            "The chicken, please"
                        ]
                    }
                ]
            }
        ]
    },
    "advanced": {
        "translation": [
            {
                "id": "adv-trans-1",
                "type": "translation",
                "title": "Subjunctive Mood",
                "content": {
                    "english": "I hope that you can come to the party.",
                    "spanish": "Espero que puedas venir a la fiesta.",
                    "words": ["Espero", "que", "puedas", "venir", "a", "la", "fiesta"]
                }
            }
        ],
        "multiple_choice": [
            {
                "id": "adv-mc-1",
                "type": "multiple_choice",
                "title": "Complex Grammar",
                "questions": [
                    {
                        "question": "Choose the correct subjunctive form: 'Quiero que ___ feliz'",
                        "options": ["eres", "seas", "serás", "ser"],
                        "correct": 1
                    }
                ]
            }
        ],
        "fill_blank": [
            {
                "id": "adv-fb-1",
                "type": "fill_blank",
                "title": "Conditional Practice",
                "sentences": [
                    {
                        "sentence": "Si tuviera tiempo, ___ al cine (ir)",
                        "correct": "iría",
                        "hint": "Conditional form of 'ir'"
                    }
                ]
            }
        ],
        "conversation": [
            {
                "id": "adv-conv-1",
                "type": "conversation",
                "title": "Job Interview",
                "dialogue": [
                    {
                        "speaker": "Interviewer",
                        "text": "¿Por qué le interesa este trabajo?",
                        "translation": "Why are you interested in this job?"
                    },
                    {
                        "speaker": "You",
                        "options": [
                            "Me apasiona este campo de trabajo",
                            "Tengo mucha experiencia en esta área",
                            "Busco nuevos desafíos profesionales"
                        ],
                        "translations": [
                            "I am passionate about this field",
                            "I have a lot of experience in this area",
                            "I'm looking for new professional challenges"
                        ]
                    }
                ]
            }
        ]
    }
}

# Add this placement test questions dictionary
placement_test = {
    "questions": [
        {
            "id": 1,
            "question": "Choose the correct translation for 'Hello, how are you?'",
            "options": [
                "Hola, ¿cómo estás?",
                "Adiós, ¿qué tal?",
                "Buenos días, ¿dónde estás?",
                "Hola, ¿dónde vas?"
            ],
            "correct": 0,
            "level": "beginner"
        },
        {
            "id": 2,
            "question": "Complete the sentence: 'Yo ___ estudiante.'",
            "options": [
                "es",
                "soy",
                "está",
                "son"
            ],
            "correct": 1,
            "level": "beginner"
        },
        {
            "id": 3,
            "question": "Which is the correct past tense of 'I went'?",
            "options": [
                "Yo voy",
                "Yo iba",
                "Yo fui",
                "Yo iré"
            ],
            "correct": 2,
            "level": "intermediate"
        },
        {
            "id": 4,
            "question": "Choose the correct subjunctive form: 'Espero que ___ bien.'",
            "options": [
                "estás",
                "estar",
                "estés",
                "esté"
            ],
            "correct": 2,
            "level": "advanced"
        },
        {
            "id": 5,
            "question": "Select the correct conditional tense: 'If I had time, I would travel.'",
            "options": [
                "Si tengo tiempo, viajo.",
                "Si tuviera tiempo, viajaría.",
                "Si tenía tiempo, viajaba.",
                "Si tendré tiempo, viajaré."
            ],
            "correct": 1,
            "level": "advanced"
        }
    ]
}

def show_hero():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>¡Bienvenidos a Español! 🇪🇸</h1>
            <p style='font-size: 1.25rem; color: #2C3E50; margin: 1rem 0;'>
                Start your Spanish learning journey today
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose Your Vibe 💫")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌱 Rookie\n(Beginner)"):
            st.session_state.current_lesson = "beginner"
            st.rerun()
    with col2:
        if st.button("💪 Skilled\n(Intermediate)"):
            st.session_state.current_lesson = "intermediate"
            st.rerun()
    with col3:
        if st.button("🔥 Pro\n(Advanced)"):
            st.session_state.current_lesson = "advanced"
            st.rerun()
    with col4:
        if st.button("✨ Find Your Level\n(Placement Test)"):
            st.session_state.placement_test_active = True
            st.rerun()

def show_lesson(level, lesson):
    lesson_id = lesson['id']
    
    # Make the back button key unique by including the lesson id
    if st.button("← Back", key=f"back_button_{lesson_id}"):
        st.session_state.current_lesson = None
        st.session_state.user_answer = []
        st.session_state.shuffled_words = None
        st.rerun()
    
    # Show completion status and last attempt
    if lesson_id in st.session_state.completed_lessons:
        st.success("✅ Completed!")
    if lesson_id in st.session_state.last_attempt_time:
        st.write(f"Last attempted: {st.session_state.last_attempt_time[lesson_id]}")
    
    st.subheader(lesson["title"])
    st.write("Translate this sentence:")
    st.info(lesson["content"]["english"])
    
    # Initialize shuffled words if needed
    if st.session_state.shuffled_words is None:
        st.session_state.shuffled_words = list(lesson["content"]["words"])
        random.shuffle(st.session_state.shuffled_words)
    
    # Now we can safely use shuffled_words since it's guaranteed to be initialized
    words = st.session_state.shuffled_words
    cols = st.columns(len(words))
    
    # Display word buttons with unique keys per lesson
    for i, word in enumerate(words):
        with cols[i]:
            # Make the key unique by including the lesson_id
            if st.button(word, key=f"word_{lesson_id}_{i}"):
                st.session_state.user_answer.append(word)
                st.rerun()
    
    # Show current translation and clear button with unique key
    current_translation = " ".join(st.session_state.user_answer)
    st.text_input("Your translation:", 
                  value=current_translation, 
                  disabled=True, 
                  key=f"translation_input_{lesson_id}")
    
    # Add clear button with unique key (already has one, but let's make it consistent)
    if st.button("Clear Translation", key=f"clear_button_{lesson_id}"):
        st.session_state.user_answer = []
        st.session_state.shuffled_words = None
        st.rerun()
    
    # Modify the Check Answer button section
    if st.button("Check Answer", key=f"check_{lesson_id}"):
        # Update last attempt time
        st.session_state.last_attempt_time[lesson_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Clean up both answers by:
        # 1. Converting to lowercase
        # 2. Removing punctuation
        # 3. Removing extra spaces
        def clean_text(text):
            # Remove punctuation and convert to lowercase
            text = text.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))
            # Remove extra spaces
            text = " ".join(text.split())
            return text
        
        user_translation = clean_text(current_translation)
        correct_translation = clean_text(lesson["content"]["spanish"])
        
        # Add to history
        attempt_result = {
            "lesson_id": lesson_id,
            "lesson_title": lesson["title"],
            "level": level,
            "timestamp": st.session_state.last_attempt_time[lesson_id],
            "correct": user_translation == correct_translation,
            "user_answer": current_translation,  # Keep original for history
            "correct_answer": lesson["content"]["spanish"]  # Keep original for history
        }
        st.session_state.lesson_history.append(attempt_result)
        
        if user_translation == correct_translation:
            st.success("¡Correcto! Well done!")
            st.session_state.completed_lessons.add(lesson_id)
            st.session_state.user_answer = []
            st.session_state.shuffled_words = None
            st.rerun()
        else:
            st.error(f"Not quite right. Try again! Make sure your answer matches: '{lesson['content']['spanish']}'")
    
    if st.button("Show Hint", key=f"hint_button_{lesson_id}"):
        st.info("Pay attention to word order and spelling.")

def show_placement_test():
    st.title("Spanish Placement Test")
    
    # Add back button
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state.placement_test_active = False
        st.session_state.current_question = 0
        st.session_state.placement_test_score = 0
        st.rerun()
    
    # Show progress
    progress = st.session_state.current_question / len(placement_test["questions"])
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question + 1} of {len(placement_test['questions'])}")
    
    if st.session_state.current_question < len(placement_test["questions"]):
        question = placement_test["questions"][st.session_state.current_question]
        
        st.subheader(question["question"])
        
        # Display options as radio buttons
        answer = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"question_{question['id']}"
        )
        
        # Submit button
        if st.button("Submit Answer", key=f"submit_{question['id']}"):
            if question["options"].index(answer) == question["correct"]:
                st.session_state.placement_test_score += 1
                st.success("¡Correcto! 🎉")
            else:
                st.error("Incorrect. The correct answer was: " + 
                        question["options"][question["correct"]])
            
            # Move to next question
            st.session_state.current_question += 1
            st.rerun()
    
    else:
        # Show results
        score = st.session_state.placement_test_score
        st.title("Test Complete!")
        st.write(f"Your score: {score} out of {len(placement_test['questions'])}")
        
        # Determine level based on score
        if score <= 1:
            recommended_level = "beginner"
            message = "We recommend starting with the Beginner level to build a strong foundation."
        elif score <= 3:
            recommended_level = "intermediate"
            message = "You show good basic knowledge. The Intermediate level would be perfect for you."
        else:
            recommended_level = "advanced"
            message = "Excellent! You're ready for the Advanced level."
        
        st.success(f"Recommended Level: {recommended_level.title()}")
        st.write(message)
        
        # Add buttons to start recommended level or return home
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Start {recommended_level.title()} Level"):
                st.session_state.current_lesson = recommended_level
                st.session_state.placement_test_active = False
                st.session_state.current_question = 0
                st.rerun()
        with col2:
            if st.button("Return to Home"):
                st.session_state.placement_test_active = False
                st.session_state.current_question = 0
                st.rerun()

def show_lesson_menu(level):
    st.title(f"{level.title()} Level - Choose Your Learning Style")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔤 Translation Exercises")
        if st.button("Practice Translation", key=f"{level}_trans"):
            st.session_state.lesson_type = "translation"
            st.rerun()
            
        st.subheader("📝 Multiple Choice")
        if st.button("Multiple Choice Questions", key=f"{level}_mc"):
            st.session_state.lesson_type = "multiple_choice"
            st.rerun()
            
        st.subheader("🎵 Audio Lessons")
        if st.button("Practice Pronunciation", key=f"{level}_audio"):
            st.session_state.lesson_type = "audio_practice"
            st.rerun()
            
        st.subheader("🎼 Learn with Songs")
        if st.button("Song Lessons", key=f"{level}_song"):
            st.session_state.lesson_type = "song_lessons"
            st.rerun()
            
    with col2:
        st.subheader("✍️ Fill in the Blanks")
        if st.button("Fill in the Blanks", key=f"{level}_fb"):
            st.session_state.lesson_type = "fill_blank"
            st.rerun()
            
        st.subheader("💭 Conversation Practice")
        if st.button("Practice Conversations", key=f"{level}_conv"):
            st.session_state.lesson_type = "conversation"
            st.rerun()
            
        st.subheader("🖼️ Picture Vocabulary")
        if st.button("Visual Learning", key=f"{level}_pic"):
            st.session_state.lesson_type = "picture_vocabulary"
            st.rerun()
            
        st.subheader("📖 Interactive Stories")
        if st.button("Story Adventures", key=f"{level}_story"):
            st.session_state.lesson_type = "interactive_stories"
            st.rerun()

def show_multiple_choice_lesson(lesson):
    lesson_id = lesson["id"]
    st.subheader(lesson["title"])
    
    # Show completion status
    if lesson_id in st.session_state.completed_lessons:
        st.success("✅ Completed!")
    if lesson_id in st.session_state.last_attempt_time:
        st.write(f"Last attempted: {st.session_state.last_attempt_time[lesson_id]}")
    
    for i, q in enumerate(lesson["questions"]):
        st.write(f"Question {i+1}: {q['question']}")
        answer = st.radio(
            "Select your answer:",
            q["options"],
            key=f"mc_{lesson_id}_{i}"
        )
        
        check_key = f"check_mc_{lesson_id}_{i}"
        if st.button("Check Answer", key=check_key):
            st.session_state.last_attempt_time[lesson_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            attempt_result = {
                "lesson_id": lesson_id,
                "lesson_title": lesson["title"],
                "level": st.session_state.current_lesson,
                "timestamp": st.session_state.last_attempt_time[lesson_id],
                "correct": q["options"].index(answer) == q["correct"],
                "user_answer": answer,
                "correct_answer": q["options"][q["correct"]]
            }
            st.session_state.lesson_history.append(attempt_result)
            
            if q["options"].index(answer) == q["correct"]:
                st.success("¡Correcto! 🎉")
                st.session_state.completed_lessons.add(lesson_id)
            else:
                st.error(f"Incorrect. The correct answer was: {q['options'][q['correct']]}")

def show_fill_blank_lesson(lesson):
    lesson_id = lesson["id"]
    st.subheader(lesson["title"])
    
    # Show completion status
    if lesson_id in st.session_state.completed_lessons:
        st.success("✅ Completed!")
    if lesson_id in st.session_state.last_attempt_time:
        st.write(f"Last attempted: {st.session_state.last_attempt_time[lesson_id]}")
    
    all_correct = True  # Track if all answers are correct
    
    for i, sentence in enumerate(lesson["sentences"]):
        st.write(sentence["sentence"])
        user_answer = st.text_input(
            "Your answer:",
            key=f"fb_{lesson_id}_{i}"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Hint", key=f"hint_{lesson_id}_{i}"):
                st.info(sentence["hint"])
        with col2:
            if st.button("Check", key=f"check_{lesson_id}_{i}"):
                st.session_state.last_attempt_time[lesson_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                is_correct = user_answer.lower().strip() == sentence["correct"].lower()
                all_correct = all_correct and is_correct
                
                attempt_result = {
                    "lesson_id": lesson_id,
                    "lesson_title": lesson["title"],
                    "level": st.session_state.current_lesson,
                    "timestamp": st.session_state.last_attempt_time[lesson_id],
                    "correct": is_correct,
                    "user_answer": user_answer,
                    "correct_answer": sentence["correct"]
                }
                st.session_state.lesson_history.append(attempt_result)
                
                if is_correct:
                    st.success("¡Correcto! 🎉")
                    if all_correct:
                        st.session_state.completed_lessons.add(lesson_id)
                else:
                    st.error(f"Incorrect. The correct answer was: {sentence['correct']}")

def show_conversation_lesson(lesson):
    lesson_id = lesson["id"]
    st.subheader(lesson["title"])
    
    # Show completion status
    if lesson_id in st.session_state.completed_lessons:
        st.success("✅ Completed!")
    if lesson_id in st.session_state.last_attempt_time:
        st.write(f"Last attempted: {st.session_state.last_attempt_time[lesson_id]}")
    
    all_responses_correct = True
    
    for i, dialogue in enumerate(lesson["dialogue"]):
        # Check if it's the system/instructor speaking
        if "text" in dialogue and "translation" in dialogue:
            with st.chat_message(dialogue["speaker"]):
                st.write(dialogue["text"])
                st.caption(dialogue["translation"])
        
        # Check if it's the user's turn to respond
        if "options" in dialogue and "translations" in dialogue:
            with st.chat_message("You"):
                response = st.radio(
                    "Choose your response:",
                    dialogue["options"],
                    key=f"conv_{lesson_id}_{i}"
                )
                if st.button("Respond", key=f"respond_{lesson_id}_{i}"):
                    st.session_state.last_attempt_time[lesson_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    idx = dialogue["options"].index(response)
                    
                    attempt_result = {
                        "lesson_id": lesson_id,
                        "lesson_title": lesson["title"],
                        "level": st.session_state.current_lesson,
                        "timestamp": st.session_state.last_attempt_time[lesson_id],
                        "correct": True,  # For conversation, we consider all responses valid
                        "user_answer": response,
                        "correct_answer": dialogue["translations"][idx]
                    }
                    st.session_state.lesson_history.append(attempt_result)
                    
                    st.success(f"Translation: {dialogue['translations'][idx]}")
                    st.session_state.completed_lessons.add(lesson_id)

def show_audio_lesson(lesson):
    st.subheader(lesson["title"])
    
    # Audio player
    st.audio(lesson["audio_url"])
    
    # Show exercises
    for ex in lesson["exercises"]:
        st.write(f"Word: {ex['word']}")
        st.write(f"Translation: {ex['translation']}")
        st.write(f"Pronunciation guide: {ex['pronunciation']}")
        
        # Add recording capability
        if st.button("Record Your Pronunciation", key=f"record_{ex['word']}"):
            st.write("Recording feature coming soon!")

def show_song_lesson(lesson):
    st.subheader(lesson["title"])
    
    # Show YouTube video
    st.video(lesson["video_url"])
    
    # Show lyrics side by side
    st.subheader("Lyrics")
    for line in lesson["lyrics"]:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🇪🇸 {line['spanish']}")
        with col2:
            st.write(f"🇬🇧 {line['english']}")
    
    # Simple practice exercises
    st.subheader("Practice")
    for i, ex in enumerate(lesson["exercises"]):
        user_answer = st.text_input(
            ex["question"],
            key=f"song_ex_{lesson['id']}_{i}"
        )
        if st.button("Check Answer", key=f"check_song_{lesson['id']}_{i}"):
            if user_answer.lower().strip() == ex["answer"].lower():
                st.success("¡Correcto! 🎉")
            else:
                st.error(f"Try again! The answer is: {ex['answer']}")

def show_picture_lesson(lesson):
    st.subheader(lesson["title"])
    
    # Show video first
    st.video(lesson["video_url"])
    
    # Show exercises
    st.subheader("Practice What You Learned")
    for i, ex in enumerate(lesson["exercises"]):
        st.write(f"Question {i+1}: {ex['question']}")
        answer = st.radio(
            "Select your answer:",
            ex["options"],
            key=f"pic_{lesson['id']}_{i}"
        )
        
        if st.button("Check Answer", key=f"check_pic_{lesson['id']}_{i}"):
            if ex["options"].index(answer) == ex["correct"]:
                st.success("¡Correcto! 🎉")
            else:
                st.error(f"Try again! The correct answer is: {ex['options'][ex['correct']]}")

def show_interactive_story(lesson):
    st.subheader(lesson["title"])
    lesson_id = lesson["id"]
    
    # Initialize story position if not exists
    if "story_position" not in st.session_state:
        st.session_state.story_position = 0
    
    # Add completion tracking
    if lesson_id in st.session_state.completed_lessons:
        st.success("✅ Completed!")
    
    # Update the story content structure
    story_content = {
        0: {
            "text": "María camina por el parque.",
            "translation": "Maria walks through the park.",
            "choices": [
                {
                    "text": "Ella ve un perro",
                    "translation": "She sees a dog",
                    "leads_to": 1
                },
                {
                    "text": "Ella compra un helado",
                    "translation": "She buys an ice cream",
                    "leads_to": 2
                }
            ]
        },
        1: {
            "text": "El perro es muy amigable.",
            "translation": "The dog is very friendly.",
            "choices": [
                {
                    "text": "Ella acaricia al perro",
                    "translation": "She pets the dog",
                    "leads_to": 3
                },
                {
                    "text": "Ella sigue caminando",
                    "translation": "She keeps walking",
                    "leads_to": 4
                }
            ]
        },
        2: {
            "text": "El helado es de chocolate.",
            "translation": "The ice cream is chocolate.",
            "choices": [
                {
                    "text": "Está delicioso",
                    "translation": "It's delicious",
                    "leads_to": 5
                },
                {
                    "text": "Está muy frío",
                    "translation": "It's very cold",
                    "leads_to": 5
                }
            ]
        },
        3: {
            "text": "¡Has llegado al final de la historia!",
            "translation": "You've reached the end of the story!",
            "is_ending": True
        },
        4: {
            "text": "¡Has llegado al final de la historia!",
            "translation": "You've reached the end of the story!",
            "is_ending": True
        },
        5: {
            "text": "¡Has llegado al final de la historia!",
            "translation": "You've reached the end of the story!",
            "is_ending": True
        }
    }
    
    # Get current scene
    current_scene = story_content[st.session_state.story_position]
    
    # Display current scene
    st.write("📖 " + current_scene["text"])
    st.caption("🔤 " + current_scene["translation"])
    
    # If it's an ending, show completion and reset option
    if current_scene.get("is_ending", False):
        st.success("¡Felicitaciones! Has completado la historia.")
        st.session_state.completed_lessons.add(lesson_id)
        if st.button("Start Over", key=f"restart_{lesson_id}"):
            st.session_state.story_position = 0
            st.rerun()
    # Otherwise show choices
    elif "choices" in current_scene:
        st.write("Choose what happens next:")
        for i, choice in enumerate(current_scene["choices"]):
            # Make key unique by including position and choice index
            if st.button(f"👉 {choice['text']}", 
                        key=f"choice_{lesson_id}_{st.session_state.story_position}_{i}",
                        help=choice["translation"]):
                st.session_state.story_position = choice["leads_to"]
                st.rerun()

def show_progress_sidebar(level=None):
    """Show progress sidebar with history and statistics"""
    with st.sidebar:
        st.title("Your Progress 📊")
        
        # Overall statistics
        total_attempts = len(st.session_state.lesson_history)
        if total_attempts > 0:
            correct_attempts = len([h for h in st.session_state.lesson_history if h["correct"]])
            accuracy = (correct_attempts / total_attempts) * 100
            
            st.metric("Total Lessons Attempted", total_attempts)
            st.metric("Success Rate", f"{accuracy:.1f}%")
            
            # Show current streak
            current_streak = 0
            for attempt in reversed(st.session_state.lesson_history):
                if attempt["correct"]:
                    current_streak += 1
                else:
                    break
            st.metric("Current Streak", f"{current_streak} ✨")
        
        # Level progress if in a specific level
        if level:
            st.subheader(f"{level.title()} Level Progress")
            level_lessons = sum(len(lessons[level][lesson_type]) for lesson_type in lessons[level])
            completed = len(st.session_state.completed_lessons)
            progress = (completed / level_lessons) * 100 if level_lessons > 0 else 0
            
            st.progress(progress / 100)
            st.write(f"Completed: {completed}/{level_lessons} lessons ({progress:.1f}%)")
        
        # Recent activity
        st.subheader("Recent Activity")
        if st.session_state.lesson_history:
            for attempt in reversed(st.session_state.lesson_history[:5]):  # Show last 5 attempts
                with st.expander(f"{attempt['lesson_title']} - {attempt['timestamp']}"):
                    st.write("Level:", attempt['level'].title())
                    st.write("Result:", "✅ Correct" if attempt['correct'] else "❌ Incorrect")
                    if not attempt['correct']:
                        st.write("Your answer:", attempt['user_answer'])
                        st.write("Correct answer:", attempt['correct_answer'])
        else:
            st.info("No activity yet. Start learning!")

def main():
    if st.session_state.placement_test_active:
        show_placement_test()
    elif st.session_state.current_lesson is None:
        show_hero()
        show_progress_sidebar()  # Show overall progress on home page
    else:
        level = st.session_state.current_lesson
        show_progress_sidebar(level)  # Show level-specific progress
        
        # Show back button to return to level selection
        if st.button("← Back to Level Selection", key="back_to_levels"):
            st.session_state.current_lesson = None  # Reset current lesson
            st.session_state.lesson_type = None    # Reset lesson type
            st.session_state.user_answer = []      # Reset any user answers
            st.session_state.shuffled_words = None # Reset shuffled words
            st.rerun()
        
        if st.session_state.lesson_type is None:
            show_lesson_menu(level)
        else:
            # Show back button to return to lesson type selection
            if st.button("← Back to Lesson Types", key="back_to_types"):
                st.session_state.lesson_type = None
                st.rerun()
            
            lesson_type = st.session_state.lesson_type
            for lesson in lessons[level][lesson_type]:
                with st.expander(f"Lesson: {lesson['title']}", expanded=True):
                    if lesson_type == "translation":
                        show_lesson(level, lesson)
                    elif lesson_type == "multiple_choice":
                        show_multiple_choice_lesson(lesson)
                    elif lesson_type == "fill_blank":
                        show_fill_blank_lesson(lesson)
                    elif lesson_type == "conversation":
                        show_conversation_lesson(lesson)
                    elif lesson_type == "audio_practice":
                        show_audio_lesson(lesson)
                    elif lesson_type == "song_lessons":
                        show_song_lesson(lesson)
                    elif lesson_type == "picture_vocabulary":
                        show_picture_lesson(lesson)
                    elif lesson_type == "interactive_stories":
                        show_interactive_story(lesson)

if __name__ == "__main__":
    main() 