import streamlit as st

def show_home():
    st.title("¡Hola Español!")
    st.markdown("### Learn Spanish the Natural Way")
    st.write("Interactive lessons tailored to your skill level")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start as Beginner"):
            st.session_state.current_level = "beginner"
            st.session_state.page = "level"
            st.experimental_rerun()
    with col2:
        if st.button("Start as Intermediate"):
            st.session_state.current_level = "intermediate"
            st.session_state.page = "level"
            st.experimental_rerun()
    with col3:
        st.button("Take Placement Test") 