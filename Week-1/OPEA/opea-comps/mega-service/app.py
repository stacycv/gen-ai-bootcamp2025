from comps import MicroService, ServiceOrchestrator, ServiceType
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.megaservice = ServiceOrchestrator()
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/process")
        async def process(request: dict):
            try:
                result = await self.megaservice.process(request)
                return JSONResponse(content=result)
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)

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

example = ExampleService()
example.add_remote_service()
app = example.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=example.host, port=example.port)