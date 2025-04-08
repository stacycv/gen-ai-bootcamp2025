import streamlit as st
from gtts import gTTS
import openai
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="Spanish Language Learning Portal",
    page_icon="🎓",
    layout="wide"
)

# Main navigation
def main():
    st.title("¡Bienvenidos! - Welcome to Spanish Learning")
    
    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose your learning activity",
        ["Home", "Vocabulary", "Grammar Practice", "Conversation", "Pronunciation"]
    )
    
    if page == "Home":
        show_home()
    elif page == "Vocabulary":
        show_vocabulary()
    elif page == "Grammar Practice":
        show_grammar()
    elif page == "Conversation":
        show_conversation()
    elif page == "Pronunciation":
        show_pronunciation()

def show_home():
    st.header("Start Your Spanish Journey")
    st.write("""
    Welcome to your AI-powered Spanish learning experience! Choose an activity from the sidebar to begin.
    
    ### Available Activities:
    - 📚 **Vocabulary**: Learn new Spanish words with interactive flashcards
    - ✍️ **Grammar Practice**: Master Spanish grammar rules
    - 💭 **Conversation**: Practice conversations with AI
    - 🗣️ **Pronunciation**: Perfect your Spanish pronunciation
    """)
    
    # Quick start section
    if st.button("Start Quick Lesson"):
        st.session_state.page = "Vocabulary"

def show_vocabulary():
    st.header("Vocabulary Practice")
    
    # Sample vocabulary words
    vocab_list = {
        "Hello": "Hola",
        "Goodbye": "Adiós",
        "Thank you": "Gracias",
        "Please": "Por favor",
        "How are you?": "¿Cómo estás?"
    }
    
    # Flashcard system
    word = st.selectbox("Choose a word to practice:", list(vocab_list.keys()))
    if st.button("Show Translation"):
        st.success(f"The Spanish translation is: {vocab_list[word]}")
        
        # Text to Speech
        tts = gTTS(vocab_list[word], lang='es')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            st.audio(fp.name)

def show_grammar():
    st.header("Grammar Practice")
    
    st.write("""
    ### Present Tense Practice
    Complete the sentences with the correct form of the verb.
    """)
    
    # Simple grammar exercise
    sentence = st.text_input("Complete: Yo ___ (hablar) español.")
    if st.button("Check Answer"):
        if sentence.lower() == "hablo":
            st.success("¡Correcto! (Correct!)")
        else:
            st.error("Try again! The correct answer is: hablo")

def show_conversation():
    st.header("Conversation Practice")
    
    st.write("Practice Spanish conversations with AI assistance!")
    user_input = st.text_input("Type your message in English or Spanish:")
    
    if st.button("Get Response"):
        # Here you would typically integrate with OpenAI API
        st.write("AI: ¡Hola! ¿Cómo puedo ayudarte hoy?")
        st.info("Note: OpenAI integration needs to be implemented")

def show_pronunciation():
    st.header("Pronunciation Practice")
    
    words = ["Hola", "Gracias", "Buenos días", "Por favor"]
    selected_word = st.selectbox("Choose a word to practice:", words)
    
    if st.button("Listen"):
        tts = gTTS(selected_word, lang='es')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            st.audio(fp.name)

if __name__ == "__main__":
    main() 