from typing import List, Tuple
import json
from tools.search_web import search_web
from tools.get_page_content import get_page_content
from tools.extract_vocabulary import extract_vocabulary
from tools.file_utils import generate_song_id, save_song_files, parse_song_request
from ollama import Client
import os
import asyncio
from functools import partial

class SongLyricsAgent:
    def __init__(self):
        print("Initializing SongLyricsAgent...")
        self.client = Client()
        self.system_prompt = self._load_prompt()
        print("Agent initialized successfully")

    def _load_prompt(self) -> str:
        """Load the system prompt from the external file."""
        print("Loading system prompt...")
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "Prompts",
            "lyrics-agent.md"
        )
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading prompt file: {e}")
            # Fallback to basic prompt if file can't be loaded
            return """You are a helpful AI assistant that helps find song lyrics and extract vocabulary.
            Follow these steps:
            1. Search for lyrics
            2. Get page content
            3. Extract vocabulary"""

    async def _call_ollama_with_timeout(self, messages, timeout=180, max_retries=1):  # 3 minutes timeout, single try
        """Call Ollama with a much longer timeout"""
        try:
            print(f"Calling Ollama (waiting up to {timeout} seconds, this might take a few minutes)...")
            print("Don't worry if it seems stuck, the model is just processing...")
            
            chat_func = partial(
                self.client.chat, 
                model="mistral",
                messages=messages,
                options={
                    "temperature": 0,
                    "num_predict": 100  # Limit response size to speed up processing
                }
            )
            
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, chat_func),
                timeout=timeout
            )
            return response
        except asyncio.TimeoutError:
            print(f"Timeout after {timeout} seconds")
            raise Exception(f"Ollama call timed out after {timeout} seconds")
        except Exception as e:
            print(f"Error calling Ollama: {str(e)}")
            raise

    async def process_request(self, message: str) -> str:
        print(f"Processing request: {message}")
        
        try:
            # Parse the song request
            print("Parsing song request...")
            song_info = parse_song_request(message)
            print(f"Song info: {song_info}")
            
            # Generate song ID early to use in error messages
            song_id = generate_song_id(song_info["artist"], song_info["song"])
            print(f"Generated song ID: {song_id}")
            
            # Initial search for lyrics
            print("Searching for lyrics...")
            urls = search_web(f"{song_info['song']} {song_info['artist']} lyrics")
            print(f"Found URLs: {urls}")
            if not urls:
                raise Exception(f"No results found for {song_info['song']} by {song_info['artist']}")

            # Get content from the first relevant URL
            print("Fetching page content...")
            content = get_page_content(urls[0])
            if not content:
                raise Exception("Could not fetch lyrics content")
            print("Successfully fetched page content")

            # Use LLM to extract clean lyrics
            print("Extracting clean lyrics using LLM...")
            content_chunk = content[:150]  # Even smaller chunk to process
            messages = [
                {
                    "role": "system", 
                    "content": "Extract lyrics. Be brief."
                },
                {
                    "role": "user", 
                    "content": f"Extract lyrics from:\n{content_chunk}"
                }
            ]
            
            print("Sending request to Ollama (this will take a few minutes)...")
            try:
                response = await self._call_ollama_with_timeout(messages)
                if not response:
                    raise Exception("Failed to get response from Ollama")
                
                clean_lyrics = response.message.content.strip()
                print("Successfully extracted clean lyrics")

                # Extract vocabulary
                print("Extracting vocabulary...")
                try:
                    vocabulary = await extract_vocabulary(clean_lyrics)
                    if not vocabulary:
                        print("Warning: No vocabulary items were extracted")
                        vocabulary = []  # Ensure we have a list even if empty
                    print(f"Found {len(vocabulary)} vocabulary items")
                except Exception as e:
                    print(f"Error in vocabulary extraction: {str(e)}")
                    vocabulary = []  # Fallback to empty list on error

                # Save files
                print("Saving files...")
                if save_song_files(song_id, clean_lyrics, vocabulary):
                    print("Files saved successfully")
                    return song_id
                else:
                    raise Exception("Failed to save song files")
                
            except Exception as e:
                print(f"Error in process_request: {str(e)}")
                raise 
        except Exception as e:
            print(f"Error in process_request: {str(e)}")
            raise 