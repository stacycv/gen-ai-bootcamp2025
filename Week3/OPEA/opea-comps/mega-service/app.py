from comps import MicroService, ServiceOrchestrator, ServiceType
import os
from fastapi import FastAPI, Request
from opea_comps.example_service import ExampleService

EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)

app = FastAPI()

class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        embedding = MicroService(
            name="embedding",
            host=EMBEDDING_SERVICE_HOST_IP,
            port=EMBEDDING_SERVICE_PORT,
            endpoint="/v1/embeddings",
            use_remote_service=True,
            service_type=ServiceType.EMBEDDING,
        )
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(embedding).add(llm)
        self.megaservice.flow_to(embedding, llm)

# Initialize the example service
example = ExampleService()
example.add_remote_service()

@app.post("/v1/example-service")
async def example_service(request: Request):
    # Get the JSON body
    body = await request.json()
    
    # Process the request using example service
    try:
        response = await example.megaservice.process(body)
        return response
    except Exception as e:
        return {"error": str(e), "details": str(type(e))}