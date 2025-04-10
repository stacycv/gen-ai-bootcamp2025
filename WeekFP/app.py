import streamlit as st
import random

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
    with col2:
        if st.button("Intermediate"):
            st.session_state.current_lesson = "intermediate"
    with col3:
        if st.button("Advanced"):
            st.session_state.current_lesson = "intermediate"
    with col4:
        st.button("Take Placement Test")

def show_lesson(level, lesson):
    # Add back button at the top
    if st.button("← Back", key="back_button"):
        st.session_state.current_lesson = None
        st.experimental_rerun()
    
    st.subheader(lesson["title"])
    st.write("Translate this sentence:")
    st.info(lesson["content"]["english"])
    
    # Initialize session state for user's answer if not exists
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = []
    
    # Randomize words if not already in session state
    if 'shuffled_words' not in st.session_state:
        st.session_state.shuffled_words = list(lesson["content"]["words"])
        random.shuffle(st.session_state.shuffled_words)
    
    # Create columns for word selection
    cols = st.columns(len(st.session_state.shuffled_words))
    
    # Display word buttons
    for i, word in enumerate(st.session_state.shuffled_words):
        with cols[i]:
            if st.button(word, key=f"word_{i}"):
                st.session_state.user_answer.append(word)
                st.experimental_rerun()
    
    # Show current translation and clear button
    current_translation = " ".join(st.session_state.user_answer)
    st.text_input("Your translation:", value=current_translation, disabled=True)
    
    # Add clear button
    if st.button("Clear Translation"):
        st.session_state.user_answer = []
        st.experimental_rerun()
    
    # Check answer button
    if st.button("Check Answer"):
        if current_translation.strip().lower() == lesson["content"]["spanish"].lower():
            st.success("¡Correcto! Well done!")
            st.session_state.completed_lessons.add(lesson["id"])
            # Reset for next attempt
            st.session_state.user_answer = []
            st.session_state.shuffled_words = None
        else:
            st.error("Not quite right. Try again!")
    
    if st.button("Show Hint"):
        st.info("Pay attention to word order and spelling.")

def main():
    # Add this at the start of main() to reset session state when changing lessons
    if 'previous_lesson' not in st.session_state:
        st.session_state.previous_lesson = None
    
    if st.session_state.current_lesson is None:
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
        
        # Show available lessons
        for lesson in lessons[level]:
            with st.expander(f"Lesson: {lesson['title']}", expanded=True):
                show_lesson(level, lesson)

if __name__ == "__main__":
    main() 