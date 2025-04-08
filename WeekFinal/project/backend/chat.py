# Japanese Language Assistant
# chat.py
from typing import Optional, Dict, Any
import random
from sentence_transformers import SentenceTransformer
import nltk
nltk.download('punkt')


class SimpleJapaneseChat:
    def __init__(self):
        """Initialize simple Japanese chat responses"""
        self.basic_responses = {
            "greetings": {
                "hello": "こんにちは (Konnichiwa)",
                "goodbye": "さようなら (Sayounara)",
                "good morning": "おはようございます (Ohayou gozaimasu)",
                "good evening": "こんばんは (Konbanwa)"
            },
            "basic_phrases": {
                "thank you": "ありがとうございます (Arigatou gozaimasu)",
                "please": "お願いします (Onegaishimasu)",
                "excuse me": "すみません (Sumimasen)",
                "you're welcome": "どういたしまして (Douitashimashite)"
            }
        }
        
        # Initialize sentence transformer for more advanced matching
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def generate_response(self, message: str) -> str:
        """Generate a simple response based on user input"""
        message = message.lower()
        
        # Check for greetings
        for key, response in self.basic_responses["greetings"].items():
            if key in message:
                return response
                
        # Check for basic phrases
        for key, response in self.basic_responses["basic_phrases"].items():
            if key in message:
                return response
        
        # Default responses for different types of questions
        if "how do you say" in message:
            return "I can help with basic Japanese phrases. Try asking about greetings or common expressions!"
            
        if "what is" in message or "what's" in message:
            return "That's an interesting question! In Japanese, it's important to consider the context. Could you provide more details?"
            
        if "explain" in message:
            return "I can explain basic Japanese concepts. What specific aspect would you like to know more about?"
            
        # Default fallback response
        return "申し訳ありません (Moushiwake arimasen). I'm a simple chat bot. Try asking about basic greetings or phrases!"


if __name__ == "__main__":
    chat = SimpleJapaneseChat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = chat.generate_response(user_input)
        print("Bot:", response)
