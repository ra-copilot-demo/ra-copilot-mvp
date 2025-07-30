# backend/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# 1. Load environment variables from .env in project root
load_dotenv()

# 2. Retrieve and validate the OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env file or your environment.")
openai.api_key = OPENAI_KEY

# 3. Instantiate the FastAPI app
app = FastAPI(title="RA Copilot Backend")

# 4. Health‑check endpoint
@app.get("/ping")
async def ping():
    return {"ping": "pong"}

# 5. Define request/response models
class AnalyzeRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    result: str

# 6. Main analysis endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    text = request.transcript.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty transcript")

    # 7. Call GPT‑4 Turbo
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or "gpt-4-turbo" depending on your subscription
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a regulatory affairs expert. "
                        "Identify any design change triggers, labeling risks, or documentation issues "
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
        # Log the exception for debugging
        print("❗ Exception in /analyze:", e)
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")

    return AnalyzeResponse(result=answer)
