from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    result: str

app = FastAPI(title="RA Copilot Backend")

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    text = request.transcript.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty transcript")
    # Stub logic: echo back
    return AnalyzeResponse(result=f"Received {len(text)} characters for analysis")
