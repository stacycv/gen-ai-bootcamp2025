from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import SongLyricsAgent

app = FastAPI()

class SongRequest(BaseModel):
    message_request: str

@app.post("/api/agent")
async def process_request(request: SongRequest):
    try:
        agent = SongLyricsAgent()
        song_id = await agent.process_request(request.message_request)
        return {"song_id": song_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Song Vocabulary API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 