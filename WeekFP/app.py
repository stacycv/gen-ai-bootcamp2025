import streamlit as st
import random
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="¡Hola Español! - Spanish Learning School",
    page_icon="🇪🇸",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #F1FAEE;
    }
    .stButton>button {
        background-color: #E63946;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 4px;
    }
    .lesson-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1D3557;
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

# Sample lesson data
lessons = {
    "beginner": [
        {
            "id": "beg-1",
            "title": "Greetings and Introductions",
            "content": {
                "english": "Hello, my name is John.",
                "spanish": "Hola, mi nombre es John.",
                "words": ["Hola", "mi", "nombre", "es", "John"]
            }
        },
        {
            "id": "beg-2",
            "title": "Numbers and Counting",
            "content": {
                "english": "I have twenty-five books.",
                "spanish": "Yo tengo veinticinco libros.",
                "words": ["yo", "tengo", "veinticinco", "libros"]
            }
        },
        {
            "id": "beg-3",
            "title": "Days of the Week",
            "content": {
                "english": "Today is Monday and tomorrow is Tuesday.",
                "spanish": "Hoy es lunes y mañana es martes.",
                "words": ["Hoy", "es", "lunes", "y", "mañana", "es", "martes"]
            }
        },
        {
            "id": "beg-4",
            "title": "Colors",
            "content": {
                "english": "The sky is blue and the grass is green.",
                "spanish": "El cielo es azul y el pasto es verde.",
                "words": ["El", "cielo", "es", "azul", "y", "el", "pasto", "es", "verde"]
            }
        },
        {
            "id": "beg-5",
            "title": "Family Members",
            "content": {
                "english": "This is my mother and my father.",
                "spanish": "Esta es mi madre y mi padre.",
                "words": ["Esta", "es", "mi", "madre", "y", "mi", "padre"]
            }
        }
    ],
    "intermediate": [
        {
            "id": "int-1",
            "title": "Past Tense",
            "content": {
                "english": "I went to the store yesterday.",
                "spanish": "Yo fui a la tienda ayer.",
                "words": ["Yo", "fui", "a", "la", "tienda", "ayer"]
            }
        },
        {
            "id": "int-2",
            "title": "Future Plans",
            "content": {
                "english": "Next week I will travel to Spain.",
                "spanish": "La próxima semana viajaré a España.",
                "words": ["La", "próxima", "semana", "viajaré", "a", "España"]
            }
        },
        {
            "id": "int-3",
            "title": "Weather Expressions",
            "content": {
                "english": "It will rain tomorrow afternoon.",
                "spanish": "Lloverá mañana por la tarde.",
                "words": ["Lloverá", "mañana", "por", "la", "tarde"]
            }
        }
    ],
    "advanced": [  # Adding advanced level
        {
            "id": "adv-1",
            "title": "Subjunctive Mood",
            "content": {
                "english": "I hope that you can come to the party.",
                "spanish": "Espero que puedas venir a la fiesta.",
                "words": ["Espero", "que", "puedas", "venir", "a", "la", "fiesta"]
            }
        },
        {
            "id": "adv-2",
            "title": "Conditional Tense",
            "content": {
                "english": "I would like to travel the world.",
                "spanish": "Me gustaría viajar por el mundo.",
                "words": ["Me", "gustaría", "viajar", "por", "el", "mundo"]
            }
        }
    ]
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
    st.title("¡Hola Español!")
    st.markdown("### Learn Spanish the Natural Way")
    st.write("Interactive lessons tailored to your skill level")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Beginner"):
            st.session_state.current_lesson = "beginner"
            st.rerun()
    with col2:
        if st.button("Intermediate"):
            st.session_state.current_lesson = "intermediate"
            st.rerun()
    with col3:
        if st.button("Advanced"):
            st.session_state.current_lesson = "advanced"
            st.rerun()
    with col4:
        if st.button("Take Placement Test"):
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
    
    # Modify the Check Answer button section to track history
    if st.button("Check Answer", key=f"check_{lesson_id}"):
        # Update last attempt time
        st.session_state.last_attempt_time[lesson_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        user_translation = " ".join(current_translation.strip().lower().split())
        correct_translation = " ".join(lesson["content"]["spanish"].lower().split())
        
        # Add to history
        attempt_result = {
            "lesson_id": lesson_id,
            "lesson_title": lesson["title"],
            "level": level,
            "timestamp": st.session_state.last_attempt_time[lesson_id],
            "correct": user_translation == correct_translation,
            "user_answer": user_translation,
            "correct_answer": correct_translation
        }
        st.session_state.lesson_history.append(attempt_result)
        
        if user_translation == correct_translation:
            st.success("¡Correcto! Well done!")
            st.session_state.completed_lessons.add(lesson_id)
            st.session_state.user_answer = []
            st.session_state.shuffled_words = None
            st.rerun()
        else:
            st.error(f"Not quite right. Try again! Make sure your answer matches exactly: '{lesson['content']['spanish']}'")
    
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

def main():
    if st.session_state.placement_test_active:
        show_placement_test()
    elif st.session_state.current_lesson is None:
        # Reset session state when returning to home
        st.session_state.user_answer = []
        st.session_state.shuffled_words = None
        st.session_state.previous_lesson = None
        show_hero()
    else:
        # Reset answer when changing lessons
        if st.session_state.previous_lesson != st.session_state.current_lesson:
            st.session_state.user_answer = []
            st.session_state.shuffled_words = None
            st.session_state.previous_lesson = st.session_state.current_lesson
            
        level = st.session_state.current_lesson
        st.sidebar.title(f"{level.title()} Level")
        
        # Show progress
        completed = len([l for l in lessons[level] if l["id"] in st.session_state.completed_lessons])
        total = len(lessons[level])
        st.sidebar.progress(completed / total)
        st.sidebar.write(f"Completed: {completed}/{total} lessons")
        
        # Show lesson history in sidebar
        if st.session_state.lesson_history:
            st.sidebar.title("Recent Activity")
            for attempt in reversed(st.session_state.lesson_history[-5:]):  # Show last 5 attempts
                with st.sidebar.expander(f"{attempt['lesson_title']} - {attempt['timestamp']}"):
                    st.write("Level:", attempt['level'])
                    st.write("Result:", "✅ Correct" if attempt['correct'] else "❌ Incorrect")
                    if not attempt['correct']:
                        st.write("Your answer:", attempt['user_answer'])
                        st.write("Correct answer:", attempt['correct_answer'])
        
        # Show available lessons
        for lesson in lessons[level]:
            with st.expander(f"Lesson: {lesson['title']}", expanded=True):
                show_lesson(level, lesson)

if __name__ == "__main__":
    main() 