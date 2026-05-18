"""
Kairos Lead Qualification API
Wraps lead_qualification_agent.py as an HTTP endpoint for n8n to call.

Endpoints:
  GET  /health       - liveness check
  POST /qualify      - qualify a lead and return scores + HubSpot/Slack payloads
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from lead_qualification_agent import process_lead_submission

app = FastAPI(
    title="Kairos Lead Qualification API",
    description="AI-powered lead scoring for Kairos Consulting",
    version="1.0.0",
)


class LeadSubmission(BaseModel):
    full_name: str
    email: str
    company_name: str
    industry: str
    budget_range: str
    timeline: str
    needs: str
    phone: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/qualify")
def qualify(lead: LeadSubmission):
    try:
        result = process_lead_submission(lead.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
