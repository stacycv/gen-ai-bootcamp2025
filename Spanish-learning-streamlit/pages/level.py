import streamlit as st
from data.lessons import lessons

def show_level():
    level = st.session_state.current_level
    
    # Header with gradient
    st.markdown('<div class="spanish-flag-gradient"></div>', unsafe_allow_html=True)
    st.title(f"{level.title()} Level")
    
    # Progress section
    st.markdown("""
    <div class="lesson-card">
        <h3>Your Progress</h3>
    """, unsafe_allow_html=True)
    
    completed = len([l for l in lessons[level] if l["id"] in st.session_state.completed_lessons])
    total = len(lessons[level])
    st.progress(completed / total)
    st.write(f"Completed: {completed}/{total} lessons")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Available lessons
    st.markdown("### Available Lessons")
    
    # Create a grid layout for lessons
    cols = st.columns(3)
    for idx, lesson in enumerate(lessons[level]):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="lesson-card">
                <h4>{lesson['title']}</h4>
                <p>{lesson['content']['english']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Lesson", key=lesson["id"]):
                st.session_state.current_lesson = lesson
                st.session_state.page = "lesson"
                st.rerun()
    
    # Navigation
    st.markdown("---")
    if st.button("← Return to Home"):
        st.session_state.page = "home"
        st.session_state.current_level = None
        st.rerun() 