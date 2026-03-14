from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

from .database import db

app = FastAPI(title="ACES MCP Server")

class ContextRequest(BaseModel):
    query_text: str
    limit: int = 5

class ContextResponse(BaseModel):
    results: list[dict]

# Simulated Embedding Function (would typically call OpenAI/SBERT)
def get_embedding(text: str) -> list[float]:
    # Placeholder: returns a random vector for demo purposes
    import random
    return [random.uniform(-1, 1) for _ in range(768)]

@app.on_event("startup")
async def startup():
    try:
        await db.connect()
    except Exception as e:
        print(f"Warning: DB Connection failed: {e}. Running in memory mode.")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "mcp-server"}

@app.post("/context", response_model=ContextResponse)
async def get_context(request: ContextRequest):
    """
    Returns relevant code/docs context for a given query.
    1. Convert query text to embedding.
    2. Query vector database (pgvector).
    3. Return results.
    """
    try:
        embedding = get_embedding(request.query_text)
        
        # If DB is not available, return mock data
        if not db.pool:
             return {
                "results": [
                    {"file_path": "mock/file.py", "content": "def mock(): pass", "distance": 0.1}
                ]
            }

        results = await db.fetch_context(embedding, request.limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("mcp_protocol:app", host="0.0.0.0", port=8000, reload=True)
