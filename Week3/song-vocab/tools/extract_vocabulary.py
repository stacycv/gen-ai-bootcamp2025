# This tool takes a body of text and will extract the vocabulary into a specific structured JSON output.

from typing import List, Dict
import re

def analyze_word(word: str) -> List[Dict]:
    """Analyze a Spanish word and break it into meaningful parts."""
    # Spanish word patterns
    patterns = {
        'verbs': {
            'ar': 'to _',
            'er': 'to _',
            'ir': 'to _'
        },
        'nouns': {
            'o': 'masculine noun',
            'a': 'feminine noun',
            'os': 'masculine plural',
            'as': 'feminine plural'
        },
        'common_words': {
            'despacito': 'slowly (diminutive)',
            'cuerpo': 'body',
            'bailar': 'to dance',
            'quiero': 'want/love',
            'ritmo': 'rhythm',
            'siente': 'feels',
            'cómo': 'how',
            'allá': 'there',
            'bajo': 'under',
            'cielo': 'sky',
            'carro': 'car',
            'llevo': 'take/carry',
            'metes': 'put/place',
            'propia': 'own',
            'discoteca': 'disco/club'
        }
    }
    
    # Check if it's a known word
    if word in patterns['common_words']:
        return [{"spanish": word, "type": "word", "meaning": patterns['common_words'][word]}]
    
    # Check verb patterns
    for ending, meaning in patterns['verbs'].items():
        if word.endswith(ending) and len(word) > len(ending):
            root = word[:-2]
            return [
                {"spanish": root, "type": "verb root"},
                {"spanish": ending, "type": "verb ending", "meaning": meaning}
            ]
    
    # Check noun patterns
    for ending, word_type in patterns['nouns'].items():
        if word.endswith(ending) and len(word) > len(ending):
            root = word[:-len(ending)]
            return [
                {"spanish": root, "type": "word root"},
                {"spanish": ending, "type": word_type}
            ]
    
    # Default case
    return [{"spanish": word, "type": "word"}]

def extract_vocabulary(text: str) -> List[Dict]:
    """Extract vocabulary words with analysis from text."""
    print("Starting vocabulary extraction from lyrics...")
    
    # Split into words and clean them
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = sorted(set(words))
    
    # Common Spanish words to skip
    skip_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'y', 'o', 'pero', 'sino',
        'de', 'del', 'en', 'por', 'para', 'con', 'a',
        'que', 'quien', 'cuyo', 'donde',
        'mi', 'tu', 'su', 'mis', 'tus', 'sus',
        'te', 'me', 'se', 'nos', 'os'
    }
    
    vocabulary = []
    for word in unique_words:
        if word not in skip_words and len(word) > 1:
            parts = analyze_word(word)
            vocab_entry = {
                "spanish": word,
                "english": parts[0].get("meaning", ""),  # Get meaning if available
                "parts": parts
            }
            vocabulary.append(vocab_entry)
    
    print(f"Found {len(vocabulary)} vocabulary words")
    return vocabulary