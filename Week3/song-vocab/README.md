# Song Vocabulary Extractor

This service finds song lyrics and extracts useful vocabulary words using AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install and run Ollama:
```bash
# On macOS
brew install ollama
ollama serve
ollama run mistral
```

3. Run the API:
```bash
python app.py
```

## Usage

Send a POST request to `/api/agent` with a song request:

```bash
curl -X POST "http://localhost:8000/api/agent" \
     -H "Content-Type: application/json" \
     -d '{"message_request": "Shape of You by Ed Sheeran"}'
```

The API will return the lyrics and extracted vocabulary words.

## Project Structure

- `app.py`: FastAPI application
- `agent.py`: ReAct agent implementation
- `tools/`: Helper tools
  - `search_web.py`: Web search using DuckDuckGo
  - `get_page_content.py`: Web page content extraction
  - `extract_vocabulary.py`: Vocabulary extraction using Mistral 

## How to run the server
```sh
uvicorn app:app --reload


### How to use the API
```sh
curl -X POST "http://localhost:8000/api/agent" \
     -H "Content-Type: application/json" \
     -d '{"message_request": "Despacito by Luis Fonsi"}'
```


