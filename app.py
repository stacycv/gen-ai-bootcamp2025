import streamlit as st

# Initialize all session state variables
if 'current_page' not in st.session_state:
    st.session_state.current_page = "level_select"
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = 1
if 'current_level' not in st.session_state:
    st.session_state.current_level = 1

# Define lesson content with more structure
def get_lesson_content(level, lesson):
    lessons = {
        1: {
            1: {
                "title": "Introduction to Level 1",
                "content": """
                Welcome to Level 1! In this lesson, you'll learn the basics.
                
                Key points:
                - Point 1
                - Point 2
                - Point 3
                """,
                "max_lessons": 3
            },
            2: {
                "title": "Level 1 - Advanced Concepts",
                "content": """
                Building on the basics, let's explore more advanced topics.
                
                Topics covered:
                - Topic 1
                - Topic 2
                - Topic 3
                """,
                "max_lessons": 3
            },
        },
        2: {
            1: {
                "title": "Welcome to Level 2",
                "content": """
                Level 2 introduces more complex concepts.
                
                We'll cover:
                - Advanced topic 1
                - Advanced topic 2
                - Advanced topic 3
                """,
                "max_lessons": 2
            },
        }
    }
    
    level_content = lessons.get(level, {})
    lesson_content = level_content.get(lesson, {})
    
    if not lesson_content:
        return {
            "title": "Content Not Found",
            "content": "This lesson is not available yet.",
            "max_lessons": 1
        }
    
    return lesson_content

def show_lesson(level, lesson):
    # Get lesson content
    lesson_data = get_lesson_content(level, lesson)
    max_lessons = lesson_data.get("max_lessons", 1)
    
    # Navigation container at the top
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("← Back to Levels", key=f"back_button_{level}_{lesson}"):
            st.session_state.current_page = "level_select"
            st.rerun()
    
    with nav_col2:
        st.title(lesson_data["title"])
    
    # Display lesson content
    st.markdown(lesson_data["content"])
    
    # Navigation buttons at the bottom
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        if lesson > 1:
            if st.button("← Previous Lesson", key=f"prev_lesson_{level}_{lesson}"):
                st.session_state.current_lesson = lesson - 1
                st.rerun()
                
    with bottom_col2:
        if lesson < max_lessons:
            if st.button("Next Lesson →", key=f"next_lesson_{level}_{lesson}"):
                st.session_state.current_lesson = lesson + 1
                st.rerun()

def main():
    # Add a header
    st.set_page_config(page_title="Learning Platform", layout="wide")
    
    if st.session_state.current_page == "level_select":
        st.title("Choose Your Learning Path")
        st.markdown("Select a level to begin your learning journey.")
        
        # Create a grid layout for level selection
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Level 1: Fundamentals", key="level_1_select"):
                st.session_state.current_page = "lesson"
                st.session_state.current_level = 1
                st.session_state.current_lesson = 1
                st.rerun()
                
        with col2:
            if st.button("Level 2: Advanced", key="level_2_select"):
                st.session_state.current_page = "lesson"
                st.session_state.current_level = 2
                st.session_state.current_lesson = 1
                st.rerun()
    else:
        show_lesson(st.session_state.current_level, st.session_state.current_lesson)

if __name__ == "__main__":
    main() 