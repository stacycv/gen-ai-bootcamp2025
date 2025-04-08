import streamlit as st

def show_home():
    # Hero Section
    st.markdown('<div class="spanish-flag-gradient"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2,1])
    with col1:
        st.title("¡Hola Español!")
        st.markdown("### Learn Spanish the Natural Way")
        st.write("Interactive lessons tailored to your skill level with our fun and effective learning platform.")
        
        # Call-to-action buttons
        col_btn1, col_btn2, col_btn3, col_space = st.columns([1,1,1,2])
        with col_btn1:
            if st.button("Start as Beginner", use_container_width=True):
                st.session_state.current_level = "beginner"
                st.session_state.page = "level"
                st.rerun()
        with col_btn2:
            if st.button("Intermediate", use_container_width=True):
                st.session_state.current_level = "intermediate"
                st.session_state.page = "level"
                st.rerun()
        with col_btn3:
            st.button("Take Test", use_container_width=True)
    
    # Features section
    st.markdown("---")
    st.markdown("### Why Learn With Us")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        <div class="lesson-card">
            <h4>Adaptive Learning</h4>
            <p>Personalized path that adapts to your progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="lesson-card">
            <h4>Interactive Exercises</h4>
            <p>Engage with practical exercises and real conversations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="lesson-card">
            <h4>Cultural Insights</h4>
            <p>Learn about Spanish culture alongside language</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col4:
        st.markdown("""
        <div class="lesson-card">
            <h4>Progress Tracking</h4>
            <p>Monitor your learning journey with detailed statistics</p>
        </div>
        """, unsafe_allow_html=True) 