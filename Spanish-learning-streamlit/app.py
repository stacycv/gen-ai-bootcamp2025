import streamlit as st
import random
from pages.home import show_home
from pages.lesson import show_lesson
from pages.level import show_level

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

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'current_level' not in st.session_state:
        st.session_state.current_level = None
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None
    if 'completed_lessons' not in st.session_state:
        st.session_state.completed_lessons = set()

    # Page routing
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'level':
        show_level()
    elif st.session_state.page == 'lesson':
        show_lesson()

if __name__ == "__main__":
    main() 