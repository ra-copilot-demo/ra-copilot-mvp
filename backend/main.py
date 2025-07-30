# backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="RA Copilot Backend")

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

class AnalyzeRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    result: str

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    text = request.transcript.strip()
    if not text:
        raise HTTPException(400, "Empty transcript")
    return AnalyzeResponse(result=f"Received {len(text)} chars")
