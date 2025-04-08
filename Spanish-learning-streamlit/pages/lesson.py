import streamlit as st

def show_lesson():
    lesson = st.session_state.current_lesson
    
    st.title(lesson["title"])
    st.write("Translate this sentence:")
    st.info(lesson["content"]["english"])
    
    # Create columns for word selection
    cols = st.columns(len(lesson["content"]["words"]))
    
    # Display word buttons
    for i, word in enumerate(lesson["content"]["words"]):
        with cols[i]:
            st.button(word, key=f"word_{i}")
    
    # Show answer input
    answer = st.text_input("Your translation:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Check Answer"):
            if answer.strip().lower() == lesson["content"]["spanish"].lower():
                st.success("¡Correcto! Well done!")
                st.session_state.completed_lessons.add(lesson["id"])
            else:
                st.error("Not quite right. Try again!")
    
    with col2:
        if st.button("Show Hint"):
            st.info("Pay attention to word order and spelling.")
    
    if st.button("Return to Level"):
        st.session_state.page = "level"
        st.session_state.current_lesson = None
        st.experimental_rerun() 