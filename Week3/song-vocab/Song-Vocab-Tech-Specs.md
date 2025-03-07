# Tech-Specs

## Business Goal
We want to be create a program that will find lyrics off the inmternet for a tarfet song in a specific language and produce vocabulary to be imported into our database.

## Technical Requirements
- Python 
- Ollama API (for LLM)
     - Mistral 7B
- Instructor (for structured JSON output)
- SQLite3 (for database)
- duckduckgo-search (for searching the web for lyrics)

### Installing Ollama
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ollama
ollama serve
ollama run mistral
```

## API Endpoints
 
 ### GetLyrics POST /api/agent 

  ### Behavior
 This endpoint goes to our agent which is designed to use the react framework so that it can go to the internet and find multiple sources of lyrics to a song and then extract the lyrics from those sources and format them into vocabulary.

Tools avaliable:
- tools/extract_vocabulary.py
- tools/get_page_content.py
- tools/search_web.py

### JSON Request Parameters
- `message_request` (str): A string that describes the song and/or artist to get lyrics for a song from the internet.

### JSON Response
- `lyrics` (str): The lyrics of the song
- `vocabulary` (list): A list of vocabulary words found in the lyrics
