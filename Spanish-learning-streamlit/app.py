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

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --spanish-red: #E63946;
        --spanish-blue: #457B9D;
        --spanish-cream: #F1FAEE;
        --spanish-navy: #1D3557;
        --spanish-yellow: #FCBF49;
    }
    
    .main {
        background-color: var(--spanish-cream);
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--spanish-red);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #d63340;
        transform: translateY(-1px);
    }
    
    /* Card styling */
    .lesson-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 16px 0;
        border: 1px solid #eee;
    }
    
    /* Typography */
    h1 {
        color: var(--spanish-navy);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2, h3 {
        color: var(--spanish-navy);
        font-weight: 600;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--spanish-red);
    }
    
    /* Info boxes */
    .stInfo {
        background-color: var(--spanish-cream);
        color: var(--spanish-navy);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
    }
    
    .stError {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Spanish flag gradient */
    .spanish-flag-gradient {
        background: linear-gradient(to right, var(--spanish-red), var(--spanish-yellow), var(--spanish-red));
        height: 4px;
        width: 100%;
        margin: 1rem 0;
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