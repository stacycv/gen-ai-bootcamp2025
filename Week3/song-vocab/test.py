import asyncio
from agent import SongLyricsAgent
import time

async def main():
    print("Starting test script...")
    start_time = time.time()
    
    agent = SongLyricsAgent()
    
    # Test with Despacito remix version
    query = "Despacito Luis Fonsi Justin Bieber letra"
    print(f"\nTrying query: {query}")
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    try:
        print("Calling process_request...")
        song_id = await agent.process_request(query)
        print(f"Success! Files saved with song_id: {song_id}")
        print(f"Check outputs/lyrics/{song_id}.txt for lyrics")
        print(f"Check outputs/vocabulary/{song_id}.json for vocabulary")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print(f"Total time elapsed: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main()) 