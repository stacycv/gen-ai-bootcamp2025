# This tool takes web content and parses ittt to extract out the target text.

import httpx
from bs4 import BeautifulSoup
import re
from typing import Optional

def get_page_content(url: str) -> Optional[str]:
    """
    Fetch and extract lyrics content from a webpage.
    
    Args:
        url (str): URL to fetch
        
    Returns:
        Optional[str]: Extracted lyrics text or None if extraction fails
    """
    try:
        # Fetch the page
        with httpx.Client(follow_redirects=True, timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()
            
        # Common lyrics container patterns
        lyrics_patterns = {
            'class_': [
                'lyrics', 'Lyrics', 'letra', 'Letra',
                'song-lyrics', 'lyricbox', 'letra-traducida',
                'letras_trad', 'lyrics-body', 'lyrics-content'
            ],
            'id': [
                'lyrics', 'Lyrics', 'letra', 'Letra',
                'lyric', 'songLyricsDiv', 'letra-traducida'
            ]
        }
        
        # Try to find lyrics container
        lyrics_element = None
        
        # Try class patterns
        for class_name in lyrics_patterns['class_']:
            lyrics_element = soup.find(class_=class_name)
            if lyrics_element:
                break
                
        # Try id patterns if no class match
        if not lyrics_element:
            for id_name in lyrics_patterns['id']:
                lyrics_element = soup.find(id=id_name)
                if lyrics_element:
                    break
        
        # If still no match, try common container elements
        if not lyrics_element:
            lyrics_element = (
                soup.find('div', class_=lambda x: x and any(pat in x.lower() for pat in ['lyric', 'letra'])) or
                soup.find('pre') or  # Some sites use <pre> tags
                soup.find('article')  # Try article if nothing else works
            )
        
        if lyrics_element:
            # Get text and clean it up
            text = lyrics_element.get_text(separator='\n')
            
            # Clean up the text
            text = _clean_lyrics(text)
            
            return text if text.strip() else None
            
        return None
        
    except Exception as e:
        print(f"Error fetching page content: {e}")
        return None

def _clean_lyrics(text: str) -> str:
    """Clean up extracted lyrics text."""
    # Remove multiple empty lines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Remove common ads/notices
    removals = [
        r'Submit Corrections',
        r'Print this Lyrics',
        r'Send .* Ringtone to your Cell',
        r'\d+ Contributors?',
        r'Lyrics Licensed & Provided by LyricFind',
        r'See More...',
        r'Download Lyrics',
        r'Add to Playlist',
        r'Share Lyrics',
        r'Report Error'
    ]
    
    for pattern in removals:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(line for line in lines if line)
    
    # Remove any remaining multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Ensure proper spacing around punctuation
    text = re.sub(r'\s*([.,!?])\s*', r'\1 ', text)
    
    # Remove any non-lyrics metadata often found at start/end
    text = re.sub(r'^.*?\n(?=[A-Z])', '', text, flags=re.DOTALL)  # Remove header
    text = re.sub(r'\n.*?$', '', text, flags=re.DOTALL)  # Remove footer
    
    return text.strip()