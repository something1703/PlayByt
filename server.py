"""
PlayByt — Token Server
FastAPI backend for Stream user-token generation and call-ID lookup.

Run with:  uvicorn server:app --port 8000
"""

import json
import os
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

STREAM_API_KEY = os.getenv("STREAM_API_KEY", "")
STREAM_API_SECRET = os.getenv("STREAM_API_SECRET", "")
CALL_ID_FILE = Path(__file__).parent / ".call_id"
HIGHLIGHTS_FILE = Path(__file__).parent / ".highlights.json"

app = FastAPI(title="PlayByt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ────────────────────────────────────────────────────────────────────


class TokenRequest(BaseModel):
    user_id: str
    user_name: str


class TokenResponse(BaseModel):
    token: str
    api_key: str


# ── Routes ────────────────────────────────────────────────────────────────────


@app.post("/api/token", response_model=TokenResponse)
def create_token(req: TokenRequest):
    """Generate a Stream Video user token signed with the API secret."""
    if not STREAM_API_SECRET:
        raise HTTPException(status_code=500, detail="STREAM_API_SECRET not configured")

    token = jwt.encode({"user_id": req.user_id}, STREAM_API_SECRET, algorithm="HS256")
    return TokenResponse(token=token, api_key=STREAM_API_KEY)


@app.get("/api/call-id")
def get_call_id():
    """Return the active Call ID written by the agent."""
    if CALL_ID_FILE.exists():
        try:
            data = json.loads(CALL_ID_FILE.read_text())
            return data
        except Exception:
            pass
    raise HTTPException(
        status_code=404,
        detail="No active call. Start the agent first: python main.py run",
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "api_key_set": bool(STREAM_API_KEY)}


@app.get("/api/highlights")
def get_highlights():
    """Return highlights logged by the agent via tool calling."""
    if HIGHLIGHTS_FILE.exists():
        try:
            data = json.loads(HIGHLIGHTS_FILE.read_text())
            return {"highlights": data}
        except Exception:
            pass
    return {"highlights": []}
