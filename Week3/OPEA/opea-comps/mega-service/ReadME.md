## How to run the LLM Service

We are using Ollama which is being delivered via docker compose.

We can set the port that the LLM will listen on. 8008 is the default but we are changing to 9000.
9000 is ideal when looking at many exisiting OPEA megaservice default ports.
```sh
LLM_ENDPOINT_PORT=9000 docker compose up 
```

When you start the Ollama, it doesnt have the model installed. So we will need to install the model via API for Ollama.

### Download (pull) the model

```sh
curl http://localhost:9000/api/pull -d '{"model": "llama3.2:1b"}'
```

### List the models




## How to run the OPEA megaservice

```sh
pip install -r requirements.txt
python app.py
```

## Testing the App

### Directory
cd Week3/OPEA/opea-comps/mega-service

### Install jq for pretty print json
```sh
for Mac
brew install jq

for Linux
sudo apt-get install jq
```

### Test the app
```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "messages": "Hello, how are you?"
  }' | jq '.' > output/$(date +%s)-response.json
```

```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Hello, this is a test message"
      }
    ],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7
  }' | jq '.' > output/$(date +%s)-response.json
```
