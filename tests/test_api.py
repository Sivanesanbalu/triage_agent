from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_triage_validation_error():
    response = client.post("/triage", json={"description": "   "})
    assert response.status_code == 422 

def test_triage_known_issue_match():
    ticket_description = "My android app keeps crashing when I open the splash screen."
    response = client.post("/triage", json={"description": ticket_description})
    
    assert response.status_code == 200
    result = response.json()
    
    assert isinstance(result["summary"], str)
    assert result["category"] == "Bug"
    assert result["severity"] == "High"
    
    assert result["is_known_issue"] == True
    assert "KB-106" in result["related_kb_ids"]
    assert "update" in result["suggested_action"].lower()

def test_triage_new_issue_fallback():
    ticket_description = "The new feature Z doesn't seem to load at all."
    response = client.post("/triage", json={"description": ticket_description})
    
    assert response.status_code == 200
    result = response.json()
    
    assert isinstance(result["summary"], str)
    assert result["is_known_issue"] == False
    assert result["related_kb_ids"] == []