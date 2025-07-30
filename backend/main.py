# backend/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Load environment variables from .env in project root
load_dotenv()

# Retrieve the OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env file.")

openai.api_key = OPENAI_KEY

# Instantiate the FastAPI app
app = FastAPI(title="RA Copilot Backend")

# Health‑check endpoint
@app.get("/ping")
async def ping():
    return {"ping": "pong"}

# Request and response models
class AnalyzeRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    result: str

# Analysis endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    text = request.transcript.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty transcript")

    # Call GPT‑4 Turbo
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-4-turbo"
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a regulatory affairs expert. "
                        "Identify any design change, labeling risk, or documentation issues "
                        "based on ISO 13485, MDR, and FDA 510(k), and suggest concise next steps."
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.2,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")

    return AnalyzeResponse(result=answer)
