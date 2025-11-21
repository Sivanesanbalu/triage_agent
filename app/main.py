from fastapi import FastAPI
from app.schemas import TicketInput, TriageResult
from app.agent import triage_ticket

app = FastAPI(
    title="Support Ticket Triage Agent",
    version="1.0.0",
    description="AI-powered service to categorize and triage support tickets."
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/triage", response_model=TriageResult)
def triage(input: TicketInput):
    return triage_ticket(input.description)
