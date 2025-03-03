import streamlit as st
from typing import Dict
import json
from collections import Counter
import re
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.chat import BedrockChat
from backend.get_transcript import YouTubeTranscriptDownloader
from backend.structured_data import TranscriptStructurer
from backend.app import generate_question
from backend.vectorstore import get_similar_questions


# Page config
st.set_page_config(
    page_title="Japanese Learning Assistant",
    page_icon="🎌",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

def render_header():
    """Render the header section"""
    st.title("🎌 Japanese Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive Japanese learning experiences.
    
    This tool demonstrates:
    - Base LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - Amazon Bedrock Integration
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with Nova",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with Nova": """
            **Current Focus:**
            - Basic Japanese learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "4. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with Nova")

    # Initialize BedrockChat instance if not in session state
    if 'bedrock_chat' not in st.session_state:
        st.session_state.bedrock_chat = BedrockChat()

    # Introduction text
    st.markdown("""
    Start by exploring Nova's base Japanese language capabilities. Try asking questions about Japanese grammar, 
    vocabulary, or cultural aspects.
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about Japanese language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Japanese?",
            "Explain the difference between は and が",
            "What's the polite form of 食べる?",
            "How do I count objects in Japanese?",
            "What's the difference between こんにちは and こんばんは?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.bedrock_chat.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})



def count_characters(text):
    """Count Japanese and total characters in text"""
    if not text:
        return 0, 0
        
    def is_japanese(char):
        return any([
            '\u4e00' <= char <= '\u9fff',  # Kanji
            '\u3040' <= char <= '\u309f',  # Hiragana
            '\u30a0' <= char <= '\u30ff',  # Katakana
        ])
    
    jp_chars = sum(1 for char in text if is_japanese(char))
    return jp_chars, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Japanese lesson YouTube URL"
    )
    
    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                downloader = YouTubeTranscriptDownloader()
                transcript = downloader.get_transcript(url)
                if transcript:
                    # Store the raw transcript text in session state
                    transcript_text = "\n".join([entry['text'] for entry in transcript])
                    st.session_state.transcript = transcript_text
                    st.success("Transcript downloaded successfully!")
                else:
                    st.error("No transcript found for this video.")
            except Exception as e:
                st.error(f"Error downloading transcript: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Raw text",
                value=st.session_state.transcript,
                height=400,
                disabled=True
            )
    
        else:
            st.info("No transcript loaded yet")
    
    with col2:
        st.subheader("Transcript Stats")
        if st.session_state.transcript:
            # Calculate stats
            jp_chars, total_chars = count_characters(st.session_state.transcript)
            total_lines = len(st.session_state.transcript.split('\n'))
            
            # Display stats
            st.metric("Total Characters", total_chars)
            st.metric("Japanese Characters", jp_chars)
            st.metric("Total Lines", total_lines)
        else:
            st.info("Load a transcript to see statistics")

def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")
    
    if not st.session_state.transcript:
        st.warning("Please load a transcript in the Raw Transcript stage first")
        return
        
    # Initialize structurer
    if 'structurer' not in st.session_state:
        st.session_state.structurer = TranscriptStructurer()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dialogue Extraction")
        
        if st.button("Process Transcript"):
            with st.spinner("Processing transcript..."):
                # Convert transcript text back to list of dicts format
                transcript_entries = [
                    {'text': line} 
                    for line in st.session_state.transcript.split('\n')
                ]
                
                # Structure the transcript
                segments = st.session_state.structurer.structure_transcript(transcript_entries)
                st.session_state.structured_segments = segments
                
                if segments:
                    st.success("Transcript processed successfully!")
                else:
                    st.error("Failed to process transcript")
        
    with col2:
        st.subheader("Structured Data")
        
        if 'structured_segments' in st.session_state:
            for i, segment in enumerate(st.session_state.structured_segments, 1):
                with st.expander(f"Segment {i}"):
                    if segment.introduction:
                        st.markdown("**Introduction:**")
                        st.write(segment.introduction)
                    
                    st.markdown("**Conversation:**")
                    for line in segment.conversation:
                        st.write(line)
                    
                    st.markdown("**Question:**")
                    st.write(segment.question)
        else:
            st.info("Click 'Process Transcript' to see structured data")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")
    
    # Query input
    query = st.text_input(
        "Test Query",
        placeholder="Enter a question about Japanese..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retrieved Context")
        # Placeholder for retrieved contexts
        st.info("Retrieved contexts will appear here")
        
    with col2:
        st.subheader("Generated Response")
        # Placeholder for LLM response
        st.info("Generated response will appear here")

def render_interactive_stage():
    """Render the interactive learning stage"""
    st.header("Interactive Learning")
    
    # Initialize question history in session state if it doesn't exist
    if 'question_history' not in st.session_state:
        st.session_state.question_history = []
    
    # Create main content and sidebar
    main_content, sidebar = st.columns([3, 1])
    
    with main_content:
        # Practice type selection
        practice_type = st.selectbox(
            "Select Practice Type",
            ["Listening Exercise", "Vocabulary Quiz", "Dialogue Practice"]
        )
        
        # Topic selection based on practice type
        topics = {
            "Listening Exercise": ["Daily Conversations", "Business Japanese", "Travel Situations", "Academic Lectures"],
            "Vocabulary Quiz": ["Basic Greetings", "Food & Dining", "Transportation", "Shopping", "Work & Office"],
            "Dialogue Practice": ["Introducing Yourself", "Asking Directions", "Restaurant Orders", "Making Appointments"]
        }
        
        selected_topic = st.selectbox(
            "Select Topic",
            topics[practice_type]
        )
        
        # Generate new question button
        if st.button("Generate New Question"):
            try:
                similar_questions = get_similar_questions(practice_type, selected_topic)
                question_data = similar_questions[0]  # Get the first question
                
                # Store in session state
                st.session_state.current_question = question_data['question']
                st.session_state.correct_answer = question_data['correct_answer']
                st.session_state.options = question_data['options']
                st.session_state.dialogue = question_data['conversation']
                st.session_state.introduction = question_data['introduction']
                st.session_state.feedback = None
                
                # Add to history with timestamp and metadata
                history_entry = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'practice_type': practice_type,
                    'topic': selected_topic,
                    'question_data': question_data
                }
                st.session_state.question_history.append(history_entry)
                
            except Exception as e:
                st.error(f"Error getting questions: {str(e)}")
        
        # Display current question
        if hasattr(st.session_state, 'current_question'):
            st.subheader("Practice Scenario")
            
            # Display introduction
            if hasattr(st.session_state, 'introduction'):
                st.markdown("**Introduction:**")
                st.write(st.session_state.introduction)
                st.markdown("---")
            
            # Display conversation
            if hasattr(st.session_state, 'dialogue'):
                st.markdown("**Conversation:**")
                for line in st.session_state.dialogue:
                    st.markdown(f"**{line['speaker']}**: {line['text']}")
                st.markdown("---")
            
            # Display question and options
            st.markdown("**Question:**")
            st.write(st.session_state.current_question)
            
            if hasattr(st.session_state, 'options'):
                selected = st.radio("Choose your answer:", st.session_state.options, key="answer")
                
                if st.button("Check Answer"):
                    if selected == st.session_state.correct_answer:
                        st.session_state.feedback = "Correct! Well done! 🎉"
                    else:
                        st.session_state.feedback = f"Not quite. The correct answer was: {st.session_state.correct_answer}"
            
            # Display feedback
            if hasattr(st.session_state, 'feedback') and st.session_state.feedback:
                if "Correct" in st.session_state.feedback:
                    st.success(st.session_state.feedback)
                else:
                    st.error(st.session_state.feedback)
    
    # Question History Sidebar
    with sidebar:
        st.header("Question History")
        
        if not st.session_state.question_history:
            st.info("No questions generated yet")
        else:
            for i, entry in enumerate(reversed(st.session_state.question_history)):
                with st.expander(f"Question {len(st.session_state.question_history) - i}"):
                    st.write(f"**Time:** {entry['timestamp']}")
                    st.write(f"**Type:** {entry['practice_type']}")
                    st.write(f"**Topic:** {entry['topic']}")
                    st.write("**Question:**")
                    st.write(entry['question_data']['question'])
                    
                    # Button to reload this question
                    if st.button("Load Question", key=f"load_{i}"):
                        question_data = entry['question_data']
                        st.session_state.dialogue = question_data['conversation']
                        st.session_state.current_question = question_data['question']
                        st.session_state.correct_answer = question_data['correct_answer']
                        st.session_state.options = question_data['options']
                        st.session_state.introduction = question_data['introduction']
                        st.session_state.feedback = None
                        st.rerun()
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.question_history = []
            st.rerun()

def main():
    render_header()
    selected_stage = render_sidebar()
    
    # Render appropriate stage
    if selected_stage == "1. Chat with Nova":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "5. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()