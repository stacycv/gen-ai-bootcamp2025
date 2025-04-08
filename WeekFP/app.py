import streamlit as st
from gtts import gTTS
import openai
import os
import tempfile
import random

# Page configuration and styling
st.set_page_config(
    page_title="¡Aprende Español!",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #fff;
    }
    .stButton>button {
        background-color: #58CC02;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 4px 0 #58A700;
        font-size: 1.2rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #58A700;
    }
    .lesson-card {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .correct-answer {
        background-color: #D7FFB8;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #58CC02;
    }
    .wrong-answer {
        background-color: #FFE1E1;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #FF4B4B;
    }
    .progress-bar {
        height: 20px;
        background-color: #E5E5E5;
        border-radius: 10px;
        margin: 10px 0;
    }
    .progress-bar-fill {
        height: 100%;
        background-color: #58CC02;
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
    }
    .lesson-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .achievement {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
    }
    
    .mascot {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 100px;
        cursor: pointer;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .bounce {
        animation: bounce 1s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'xp_points' not in st.session_state:
    st.session_state.xp_points = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = 1
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 50

def award_achievement(title):
    if title not in st.session_state.achievements:
        st.session_state.achievements.append(title)
        st.balloons()
        st.success(f"🏆 New Achievement Unlocked: {title}")

def show_mascot():
    st.markdown("""
        <img src="assets/images/owl.png" class="mascot bounce" 
        onclick="alert('¡Hola! Keep learning!')" />
    """, unsafe_allow_html=True)

def main():
    # Top bar with XP and streak
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.markdown(f"### 🔥 Streak: {st.session_state.streak} days")
    with col2:
        st.markdown(f"### ⭐ XP: {st.session_state.xp_points} points")
    with col3:
        st.markdown(f"### 📚 Level {st.session_state.current_lesson}")
    
    # Progress bar
    progress = (st.session_state.xp_points % 100) / 100
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress * 100}%"></div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.image("assets/images/logo.png", width=100)  # We'll create this logo
        
        # Add daily goal progress
        st.markdown("### Daily Goal")
        goal_progress = (st.session_state.xp_points % st.session_state.daily_goal) / st.session_state.daily_goal * 100
        st.progress(goal_progress)
        st.write(f"{int(goal_progress)}% of daily goal")

    # Show achievements
    if st.session_state.achievements:
        st.markdown("### 🏆 Achievements")
        for achievement in st.session_state.achievements:
            st.markdown(f"""
                <div class="achievement">
                    {achievement}
                </div>
            """, unsafe_allow_html=True)

    page = st.radio(
        "Choose your activity",
        ["Lessons", "Practice", "Stories", "Review"],
        key="navigation"
    )

    if page == "Lessons":
        show_lessons()
    elif page == "Practice":
        show_practice()
    elif page == "Stories":
        show_stories()
    elif page == "Review":
        show_review()

def show_lessons():
    st.markdown("## 📚 Available Lessons")
    
    lessons = [
        {"title": "Basics 1", "icon": "👋", "description": "Learn basic greetings and phrases"},
        {"title": "Family", "icon": "👨‍👩‍👧‍👦", "description": "Learn family-related vocabulary"},
        {"title": "Food", "icon": "🍽️", "description": "Learn food and restaurant vocabulary"},
    ]

    for i, lesson in enumerate(lessons, 1):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div class="lesson-card">
                    <h3>{lesson['icon']} {lesson['title']}</h3>
                    <p>{lesson['description']}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(f"Start {i}", key=f"lesson_{i}"):
                start_lesson(lesson['title'])

def start_lesson(lesson_title):
    st.session_state.current_lesson = lesson_title
    show_exercise()

def show_exercise():
    st.markdown(f"## {st.session_state.current_lesson}")
    
    # Sample exercise
    exercise_type = random.choice(["multiple_choice", "translation", "matching"])
    
    if exercise_type == "multiple_choice":
        st.markdown("### Choose the correct translation")
        question = "How do you say 'Hello' in Spanish?"
        options = ["Hola", "Adiós", "Gracias", "Por favor"]
        
        for option in options:
            if st.button(option):
                if option == "Hola":
                    show_correct_answer()
                else:
                    show_wrong_answer()

def show_correct_answer():
    st.markdown("""
        <div class="correct-answer bounce">
            ¡Correcto! +10 XP
        </div>
    """, unsafe_allow_html=True)
    st.session_state.xp_points += 10
    
    # Check for achievements
    if st.session_state.xp_points >= 100:
        award_achievement("Centurion - Earn 100 XP")
    if st.session_state.streak >= 7:
        award_achievement("Week Warrior - 7 day streak")
        
    st.balloons()

def show_wrong_answer():
    st.markdown("""
        <div class="wrong-answer">
            ¡Inténtalo de nuevo! (Try again!)
        </div>
    """, unsafe_allow_html=True)

def show_practice():
    st.markdown("## 🎯 Practice")
    practice_types = ["Vocabulary", "Grammar", "Pronunciation", "Conversation"]
    
    for practice in practice_types:
        st.markdown(f"""
            <div class="lesson-card">
                <h3>{practice}</h3>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Start {practice}"):
            st.session_state.current_practice = practice

def show_stories():
    st.markdown("## 📖 Stories")
    st.markdown("""
        Practice Spanish with interactive stories!
        Choose your difficulty level:
    """)
    
    story_levels = ["Beginner", "Intermediate", "Advanced"]
    for level in story_levels:
        if st.button(level):
            st.write(f"Loading {level} story...")

def show_review():
    st.markdown("## 📝 Review")
    st.markdown("Review your recent lessons and track your progress")
    
    # Sample progress chart
    progress_data = {
        "Vocabulary": 80,
        "Grammar": 65,
        "Pronunciation": 90,
        "Overall": 78
    }
    
    for category, progress in progress_data.items():
        st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: {progress}%"></div>
            </div>
            {category}: {progress}%
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_mascot() 