from urllib.parse import quote
import os
import json
from typing import Dict, List

def generate_song_id(artist: str, song: str) -> str:
    """
    Generate a URL-safe song ID from artist and song name.
    
    Args:
        artist (str): Artist name
        song (str): Song title
        
    Returns:
        str: URL-safe song ID
    """
    # Remove special characters and convert to lowercase
    safe_string = f"{artist}-{song}".lower()
    safe_string = ''.join(c for c in safe_string if c.isalnum() or c in ' -')
    safe_string = safe_string.replace(' ', '-')
    return quote(safe_string)

def save_song_files(song_id: str, lyrics: str, vocabulary: List[Dict]) -> bool:
    """
    Save lyrics and vocabulary to their respective files.
    
    Args:
        song_id (str): Generated song ID
        lyrics (str): Song lyrics
        vocabulary (List[Dict]): List of vocabulary words in format:
            {
                "spanish": str,      # Spanish word
                "english": str,      # English translation
                "parts": List[Dict]  # Word parts for learning
            }
        
    Returns:
        bool: True if files were saved successfully
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        
        # Save lyrics
        lyrics_path = os.path.join(base_dir, "outputs", "lyrics", f"{song_id}.txt")
        with open(lyrics_path, "w", encoding="utf-8") as f:
            f.write(lyrics)
            
        # Save vocabulary in structured format
        vocab_path = os.path.join(base_dir, "outputs", "vocabulary", f"{song_id}.json")
        vocab_data = {
            "song_id": song_id,
            "vocabulary": [
                {
                    "spanish": word["spanish"],
                    "english": word["english"],
                    "parts": word["parts"]
                }
                for word in vocabulary
            ]
        }
        with open(vocab_path, "w", encoding="utf-8") as f:
            json.dump(vocab_data, f, indent=2, ensure_ascii=False)
            
        print(f"Vocabulary to be saved: {vocabulary}")
        
        return True
    except Exception as e:
        print(f"Error saving files: {e}")
        return False

def parse_song_request(message: str) -> Dict[str, str]:
    """
    Parse the song request to extract artist and song name.
    
    Args:
        message (str): User's song request message
        
    Returns:
        Dict[str, str]: Dictionary containing 'artist' and 'song'
    """
    # Handle common formats like "Song by Artist" or "Artist - Song"
    if " by " in message:
        song, artist = message.split(" by ", 1)
    elif " - " in message:
        artist, song = message.split(" - ", 1)
    else:
        # Default to treating the whole message as the song title
        return {"artist": "unknown", "song": message}
    
    return {
        "artist": artist.strip(),
        "song": song.strip()
    } 