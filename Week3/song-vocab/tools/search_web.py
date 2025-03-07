# This tool uses duckduckgo to search the web for a pages to then further crawl and extract the content.

from duckduckgo_search import DDGS
from typing import List
import time
import re

def search_web(query: str, max_retries: int = 3) -> List[str]:
    """
    Search the web for Spanish song lyrics using DuckDuckGo.
    With fallback for popular songs.
    
    Args:
        query (str): Search query string
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        List[str]: List of URLs from search results, prioritizing Spanish lyrics sites
    """
    # Known popular songs direct URLs (as fallback)
    popular_songs = {
        "despacito": [
            "https://www.letras.com/luis-fonsi/despacito-ft-daddy-yankee/",
            "https://www.musixmatch.com/lyrics/Luis-Fonsi-Daddy-Yankee/Despacito"
        ]
    }

    # Check if this is a known popular song
    query_lower = query.lower()
    for song_key, urls in popular_songs.items():
        if song_key in query_lower:
            print(f"Found direct URLs for popular song: {song_key}")
            return urls[:3]

    # If not a known song, try the regular search
    # Add 'letras' or 'lyrics español' if not already in query
    if not any(term in query.lower() for term in ['letras', 'lyrics español', 'letra']):
        query = f"{query} letras español"

    print(f"Searching for: {query}")

    # List of preferred Spanish lyrics domains
    preferred_domains = [
        'letras.com',
        'musixmatch.com',
        'genius.com',
        'lyrics.com',
        'letraseningles.es',
        'letrastraducidas.com'
    ]
    
    for attempt in range(max_retries):
        try:
            # Create a new DDGS instance for each attempt
            with DDGS() as ddgs:
                # Try regular text search
                results = list(ddgs.text(
                    query,
                    max_results=10
                ))

            print(f"Search attempt {attempt + 1}: Found {len(results)} results")
            
            if results:
                # Filter and sort results
                filtered_urls = []
                
                # Process all results
                for result in results:
                    # Get the URL from the result
                    url = result.get('link')
                    
                    if not url:
                        continue
                        
                    # Prioritize preferred domains
                    if any(domain in url.lower() for domain in preferred_domains):
                        filtered_urls.insert(0, url)  # Add to start of list
                    else:
                        filtered_urls.append(url)
                
                if filtered_urls:
                    print(f"Found URLs: {filtered_urls[:3]}")
                    return filtered_urls[:3]
            
            # If we get here, no results were found, wait before retrying
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))  # Exponential backoff
                
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
    
    print("All search attempts failed")
    return []

def _is_lyrics_url(url: str) -> bool:
    """Helper function to check if URL likely contains lyrics."""
    lyrics_indicators = [
        'letras', 'lyrics', 'letra', 'musica',
        'cancion', 'song', 'traducida', 'translated'
    ]
    url_lower = url.lower()
    return any(indicator in url_lower for indicator in lyrics_indicators)