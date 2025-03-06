# OPEA Components

Description of what this project does and its purpose.

## Getting Started

### Choosing a Model

You can get the model_id that ollama will launch from the [Ollama Library](https://ollama.com/library).

https://ollama.com/library/llama3.2

eg.https://ollama.com/library/llama3.2

### Prerequisites

- Docker
- Docker Compose

### Environment Variables

The following environment variables are required:
- `LLM_ENDPOINT_PORT`: Set to 8008
- `LLM_MODEL_ID`: Set to "llama3.21b"
- `host_ip`: Your host IP address (e.g., 192.168.1.100)

## Generate a Request

curl http://localhost:11434/api/generate -d '{
    "model": "llama3.2:1B",
    "prompt": "why is the sky blue?"
}'



curl http://localhost:11434/api/generate -d '{
    "model": "llama3.2:1B",
    "prompt": "Give me a simple recipe for chocolate chip cookies"
}'

