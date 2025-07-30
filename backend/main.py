import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Instantiate the FastAPI app first
app = FastAPI(title="RA Copilot Backend")

# Optional health-check
@app.get("/ping")
async def ping():
    return {"ping": "pong"}

# Load OpenAI API key
# For local dev, make sure you set environment var OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request/response models
class AnalyzeRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    result: str

# Register the /analyze endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    text = request.transcript.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty transcript")

    # Call GPT-4 Turbo
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",              # or "gpt-4-turbo"
            messages=[
                {"role": "system", "content": (
                    "You are a regulatory affairs expert. "
                    "Identify any design change, labeling risk, or documentation issues "
                    "based on ISO 13485, MDR, and FDA 510(k)."
                )},
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.2,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")

    return AnalyzeResponse(result=answer)

