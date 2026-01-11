from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime, date

from financial_analysis import get_user_financial_summary
from chat_with_coach import query_coach

app = FastAPI(title="Finance Coach API")

# CORS for local dev (Vite default port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/financial-summary")
def financial_summary(user_id: str):
    try:
        summary = get_user_financial_summary(user_id)

        # Convert pandas Timestamps to ISO strings for JSON serialization
        for tx in summary.get("recent_transactions", []):
            d = tx.get("date")
            if isinstance(d, (pd.Timestamp, datetime, date)):
                tx["date"] = d.isoformat()

        for ch in summary.get("recent_gray_charges", []):
            d = ch.get("last_charge_date")
            if isinstance(d, (pd.Timestamp, datetime, date)):
                ch["last_charge_date"] = d.isoformat()

        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = query_coach(req.user_id, req.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# If running with: python server.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
