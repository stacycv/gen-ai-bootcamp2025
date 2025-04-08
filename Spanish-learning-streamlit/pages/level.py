import streamlit as st
from data.lessons import lessons

def show_level():
    level = st.session_state.current_level
    st.title(f"{level.title()} Level")
    
    # Show progress
    completed = len([l for l in lessons[level] if l["id"] in st.session_state.completed_lessons])
    total = len(lessons[level])
    st.progress(completed / total)
    st.write(f"Completed: {completed}/{total} lessons")
    
    # Show available lessons
    for lesson in lessons[level]:
        with st.expander(f"Lesson: {lesson['title']}", expanded=True):
            st.write(lesson["content"]["english"])
            if st.button("Start Lesson", key=lesson["id"]):
                st.session_state.current_lesson = lesson
                st.session_state.page = "lesson"
                st.experimental_rerun()
    
    if st.button("Return to Home"):
        st.session_state.page = "home"
        st.session_state.current_level = None
        st.experimental_rerun() 