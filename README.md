# Support Ticket Triage Agent

This project implements a FastAPI service that analyzes support ticket descriptions, identifies their category and severity, checks for known issues using a small knowledge base, and suggests an appropriate action. The service takes a free-text input and returns structured output.

---

## How to Run the Project

### 1. Prerequisites

* Python 3.10 or higher
* pip
* (Optional) Docker

---

## 2. Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables (optional)

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=dummy_key
LLM_MODEL_NAME=gpt-4o-mini
```

The current implementation uses rule-based logic, but the structure is prepared so a real LLM can be integrated later.

---


## 4. Running the Server

Start the server with:

```
uvicorn app.main:app --reload
```

Open the interactive API documentation in your browser:

```
http://127.0.0.1:8000/docs
```

---

## Testing the API

You can test the `/triage` endpoint using the Swagger UI or the following curl command:

```
curl -X POST "http://127.0.0.1:8000/triage" \
     -H "Content-Type: application/json" \
     -d '{
           "description": "My android app keeps crashing when I open the splash screen."
         }'
```

Expected example response:

```
{
  "summary": "Application crash detected",
  "category": "Bug",
  "severity": "High",
  "is_known_issue": true,
  "related_kb_ids": ["KB-106"],
  "suggested_action": "Known bug in v2.4. Ask the user to update to v2.4.1."
}
```

---

## Project Structure

```
support-ticket-triage/
│
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── agent.py          # Core triage agent logic (LLM + rules)
│   ├── kb_tool.py        # Knowledge-base search tool
│   └── schemas.py        # Pydantic request/response models
│
├── data/
│   └── knowledge_base.json   # Sample KB with known issues
│
├── tests/
│   └── test_api.py       # Basic API tests for /triage endpoint
│
├── Dockerfile            # Container setup for deployment
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```


## How the Agent Works

1. The API receives a ticket description through the `/triage` endpoint.
2. The agent identifies the summary, category, and severity using simple rule-based logic.
3. The knowledge base tool searches for matching known issues using keyword comparison.
4. If a related known issue exists, the agent marks the ticket as a known issue and returns the suggested action from the knowledge base.
5. If there is no match, the agent provides a general recommended action.

The agent and tool modules are separated so the rule-based logic can be replaced later with an LLM without modifying the API layer.

---

## Running Tests

```
pytest
```

---

## Docker Usage (Optional)

Build the Docker image:

```
docker build -t triage-agent .
```

Run the service in a container:

```
docker run -p 8000:8000 triage-agent
```

---

## Production Considerations

* Environment-based configuration for easy deployment
* Stateless design suitable for scaling
* Clear separation of modules for maintainability
* Ready for integration with real LLMs and vector search
* Can be deployed with Docker on services like AWS ECS, GCP Cloud Run, or Azure App Service

---

