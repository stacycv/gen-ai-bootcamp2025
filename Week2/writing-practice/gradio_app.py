import gradio as gr
import requests
import logging
import random
import yaml
from typing import Dict, Tuple
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='app_debug.log',  # Changed from gradio_app.log
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # This ensures our configuration takes precedence
)
logger = logging.getLogger(__name__)

# Add a console handler to see logs in terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class SpanishWritingApp:
    def __init__(self):
        logger.info("Initializing SpanishWritingApp")
        self.vocabulary = None
        self.current_sentence = None
        self.load_prompts()
        
    def load_prompts(self):
        """Load prompts from YAML file"""
        try:
            with open('prompts.yaml', 'r') as file:
                self.prompts = yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")
            self.prompts = {}

    def load_vocabulary(self, group_id: str) -> str:
        """Fetch vocabulary from API and return a random word"""
        logger.info(f"Attempting to load vocabulary for group_id: '{group_id}'")
        
        if not group_id or group_id.strip() == "":
            logger.warning("Empty group_id provided")
            return "Please enter a Group ID"
        
        try:
            url = f'http://localhost:5001/api/groups/{group_id}/words/raw'
            logger.info(f"Making API request to: {url}")
            
            try:
                response = requests.get(url, timeout=5)
                
                try:
                    response_data = response.json()
                    
                    # Validate response structure
                    if not isinstance(response_data, dict):
                        raise ValueError("Response is not a dictionary")
                    if "words" not in response_data:
                        raise ValueError("Response missing 'words' field")
                    if not isinstance(response_data["words"], list):
                        raise ValueError("'words' field is not a list")
                    
                    self.vocabulary = response_data
                    
                    # Pick a random word and return just the Spanish word
                    random_word = random.choice(self.vocabulary['words'])
                    return random_word['spanish']  # Return just the word
                    
                except json.JSONDecodeError as e:
                    return "Error loading vocabulary"
                except ValueError as e:
                    return "Invalid vocabulary data"
                
            except requests.exceptions.ConnectionError as e:
                return "Could not connect to API"
            except requests.exceptions.Timeout:
                return "Request timed out"
            
        except Exception as e:
            return "Error loading vocabulary"

    def generate_sentence(self) -> Tuple[str, str, str]:
        """Generate a new sentence using a random word"""
        logger.info("Starting sentence generation")
        
        if not self.vocabulary or not self.vocabulary.get('words'):
            logger.error("No vocabulary loaded")
            return "", "", "Error: Please load vocabulary first"

        try:
            # Pick a random word from vocabulary
            word = random.choice(self.vocabulary['words'])
            spanish_word = word.get('spanish', '')
            english_word = word.get('english', '')
            logger.info(f"Selected word: {spanish_word} ({english_word})")
            
            # Pick a template that makes sense for the word type
            template = random.choice(SPANISH_TEMPLATES)
            
            # Generate Spanish sentence
            spanish_sentence = template.format(
                object=spanish_word,
                timeframe=random.choice(SPANISH_TIMEFRAMES)
            )
            logger.debug(f"Generated Spanish sentence: {spanish_sentence}")
            
            # Create English translation
            english_sentence = spanish_sentence
            
            # Replace longest phrases first to avoid partial replacements
            sorted_translations = sorted(
                TRANSLATIONS.items(), 
                key=lambda x: len(x[0]), 
                reverse=True
            )
            
            for spanish, english in sorted_translations:
                english_sentence = english_sentence.replace(spanish, english)
            
            # Replace the vocabulary word last
            english_sentence = english_sentence.replace(spanish_word, english_word)
            
            # Clean up any double spaces
            english_sentence = ' '.join(english_sentence.split())
            spanish_sentence = ' '.join(spanish_sentence.split())
            
            logger.debug(f"Generated English sentence: {english_sentence}")
            
            # Store both sentences
            self.spanish_sentence = spanish_sentence
            self.current_sentence = english_sentence
            
            return spanish_sentence, english_sentence, "Sentence generated successfully"
            
        except Exception as e:
            logger.error(f"Error generating sentence: {e}", exc_info=True)
            return "", "", f"Error generating sentence: {str(e)}"

    def grade_submission(self, written_text: str) -> Tuple[str, str, str, str]:
        """Grade the submitted text"""
        if not self.spanish_sentence:  # Check for Spanish sentence instead
            return "", "", "", "Error: No sentence to grade against"

        try:
            written_text = written_text.strip().lower()
            expected_spanish = self.spanish_sentence.lower()  # Use spanish_sentence instead of current_sentence
            
            # Calculate similarity
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, written_text, expected_spanish).ratio()
            
            # Find specific differences
            differences = []
            if written_text != expected_spanish:
                # Check for missing words
                expected_words = set(expected_spanish.split())
                written_words = set(written_text.split())
                missing = expected_words - written_words
                extra = written_words - expected_words
                
                if missing:
                    differences.append(f"Missing words: {', '.join(missing)}")
                if extra:
                    differences.append(f"Extra words: {', '.join(extra)}")
            
            # More lenient grading
            if written_text == expected_spanish:  # Exact match
                grade = "A"
                feedback = "¡Perfecto! Your answer matches exactly!"
            elif similarity > 0.9:
                grade = "A"
                feedback = "¡Excelente! (Excellent!) Your sentence is nearly perfect."
            elif similarity > 0.8:
                grade = "A-"
                feedback = "¡Muy bien! (Very good!) Just a few small differences:"
            elif similarity > 0.6:
                grade = "B"
                feedback = "¡Buen intento! (Good try!) Here's what to check:"
            elif similarity > 0.4:
                grade = "C"
                feedback = "Keep practicing! Here's what needs work:"
            else:
                grade = "D"
                feedback = "Let's review the sentence structure. Here's what's different:"
            
            # Add specific differences to feedback if not perfect
            if written_text != expected_spanish and differences:
                feedback += "\n- " + "\n- ".join(differences)
            
            # Add comparison
            feedback += "\n\nExpected: " + expected_spanish
            feedback += "\nYou wrote: " + written_text
            
            return (
                written_text,      # what was typed
                expected_spanish,  # what was expected (Spanish sentence)
                grade,            # letter grade
                feedback          # detailed feedback
            )
            
        except Exception as e:
            logger.error(f"Error grading submission: {e}", exc_info=True)
            return "", "", "", f"Error: {str(e)}"

# Add this after the class definition but before generate_sentence method

SPANISH_TEMPLATES = [
    # Simple present tense
    "Me gusta {object}.",  # I like the [object]
    "Tengo {object}.",     # I have [object]
    "Necesito {object}.",  # I need [object]
    "Quiero {object}.",    # I want [object]
    
    # Present continuous
    "Estoy usando {object}.",     # I am using [object]
    "Estoy mirando {object}.",    # I am looking at [object]
    
    # Simple location statements
    "El {object} está en la mesa.",     # The [object] is on the table
    "Mi {object} está aquí.",           # My [object] is here
    "Hay {object} en la cocina.",       # There is [object] in the kitchen
    
    # Future tense with 'going to'
    "{timeframe} voy a comprar {object}.",  # [timeframe] I am going to buy [object]
    "{timeframe} voy a usar {object}.",     # [timeframe] I am going to use [object]
]

SPANISH_TIMEFRAMES = [
    "hoy",           # today
    "mañana",        # tomorrow
    "esta tarde",    # this afternoon
    "esta noche",    # tonight
    "el lunes",      # on Monday
    "el fin de semana"  # on the weekend
]

TRANSLATIONS = {
    # Template translations
    "Me gusta": "I like",
    "Tengo": "I have",
    "Necesito": "I need",
    "Quiero": "I want",
    "Estoy usando": "I am using",
    "Estoy mirando": "I am looking at",
    "está en la mesa": "is on the table",
    "está aquí": "is here",
    "Hay": "There is",
    "en la cocina": "in the kitchen",
    "voy a comprar": "am going to buy",
    "voy a usar": "am going to use",
    "Mi": "My",
    "El": "The",
    "La": "The",
    
    # Timeframe translations
    "hoy": "today",
    "mañana": "tomorrow",
    "esta tarde": "this afternoon",
    "esta noche": "tonight",
    "el lunes": "on Monday",
    "el fin de semana": "on the weekend"
}

def create_app():
    app = SpanishWritingApp()
    
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("# Spanish Writing Practice")
        
        # Updated instructions
        gr.Markdown("""
        ### 🎯 Goal: Copy the Spanish sentence you see, then check your accuracy
        ### 📝 Steps:
        1. Load a vocabulary group
        2. Click 'Generate New Sentence' to see a Spanish sentence
        3. Practice writing the Spanish sentence exactly as shown
        """)
        
        with gr.Row():
            gr.Markdown("""
            ### Available Groups:
            1. Basic Spanish Words
            2. Food and Drinks
            3. Animals
            4. Colors
            """)
        
        with gr.Row():
            group_id_input = gr.Textbox(
                label="Group ID",
                placeholder="Enter group number (1-4)",
                value="1",
                scale=2
            )
            load_btn = gr.Button("Load Vocabulary", scale=1)
            status_text = gr.Textbox(
                label="Status",
                interactive=False,
                scale=3,
                show_label=False  # Hide the "Status" label
            )
        
        with gr.Row():
            generate_btn = gr.Button(
                "Generate New Sentence",
                variant="primary"  # Make it stand out
            )
        
        with gr.Row():
            spanish_output = gr.Textbox(
                label="Spanish Sentence to Copy ✍️",
                interactive=False,
                scale=1
            )
            english_output = gr.Textbox(
                label="English Translation (for reference)",
                interactive=False,
                scale=1
            )
            
        with gr.Row():
            written_input = gr.Textbox(
                label="Write the Spanish sentence here",
                placeholder="Type the Spanish sentence you see above...",
                scale=3
            )
            submit_btn = gr.Button("Submit for Review")
            
        with gr.Row():
            transcription_output = gr.Textbox(label="Your Text", interactive=False)
            translation_output = gr.Textbox(label="Expected Text", interactive=False)
            grade_output = gr.Textbox(label="Grade", interactive=False)
            feedback_output = gr.Textbox(label="Feedback", interactive=False)
            
        # Event handlers
        load_btn.click(
            fn=app.load_vocabulary,
            inputs=[group_id_input],
            outputs=[status_text]
        )
        
        generate_btn.click(
            app.generate_sentence,
            inputs=[],
            outputs=[spanish_output, english_output, status_text]
        )
        
        submit_btn.click(
            app.grade_submission,
            inputs=[written_input],
            outputs=[transcription_output, translation_output, grade_output, feedback_output]
        )
        
    return interface

if __name__ == "__main__":
    demo = create_app()
    demo.launch(server_name="localhost", server_port=7860)
