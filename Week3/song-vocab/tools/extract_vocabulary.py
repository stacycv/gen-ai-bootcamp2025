# This tool takes a body of text and will extract the vocabulary into a specific structured JSON output.

from typing import List, Dict
import re

def extract_vocabulary(text: str) -> List[Dict]:
    """
    Extract vocabulary words from the clean lyrics text.
    
    Args:
        text (str): Clean lyrics text to extract vocabulary from
        
    Returns:
        List[Dict]: List of vocabulary words with their details
    """
    print("Starting vocabulary extraction from clean lyrics...")
    
    # Split into words and clean them
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove duplicates and sort
    unique_words = sorted(set(words))
    
    # Common Spanish words to skip
    skip_words = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',  # articles
        'y', 'o', 'pero', 'sino',  # conjunctions
        'de', 'del', 'en', 'por', 'para', 'con', 'a',  # prepositions
        'que', 'quien', 'cuyo', 'donde',  # relative pronouns
        'mi', 'tu', 'su', 'mis', 'tus', 'sus'  # possessives
    }
    
    # Create vocabulary list
    vocabulary = []
    for word in unique_words:
        if word not in skip_words and len(word) > 1:  # Skip common words and single letters
            vocab_entry = {
                "spanish": word,
                "english": "",  # Leave translation empty for now
                "parts": [
                    {
                        "spanish": word,
                        "type": "word"
                    }
                ]
            }
            vocabulary.append(vocab_entry)
    
    print(f"Found {len(vocabulary)} unique vocabulary words")
    return vocabulary