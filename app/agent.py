# app/agent.py

# Import schemas and the KB tool
from app.schemas import TriageResult, Category, Severity
from app.kb_tool import kb_tool # <-- Import the tool

def triage_ticket(description: str) -> TriageResult:
    """
    Orchestrates the triage process:
    1. Search the Knowledge Base.
    2. Determine ticket fields (Summary, Category, Severity, Action)
       (In a real agent, this would be done by an LLM).
    """
    
    # --- 1. Tool Call: Search Knowledge Base ---
    
    # Search the KB for related issues
    known_issues = kb_tool.search(description)
    
    is_known_issue = len(known_issues) > 0
    related_kb_ids = [issue['id'] for issue in known_issues]
    
    # --- 2. Orchestration/Decision Logic (Simulating LLM) ---
    
    # If a known issue is found, use its resolution and category/title
    if is_known_issue:
        top_issue = known_issues[0]
        
        # Use KB data for suggestions
        suggested_action = top_issue['resolution']
        
        # This part should ideally use an LLM, but for the demo,
        # we will extract/infer the fields from the most relevant KB item/ticket
        summary = f"Known issue: {top_issue['title']}"
        
        # Map KB category string to your Category enum
        # You'll need to make sure the strings match the enums in schemas.py
        category_str = top_issue.get('category', 'OTHER').upper() 
        try:
            category = Category[category_str]
        except KeyError:
            category = Category.OTHER
            
        # Default high severity for known bugs requiring specific resolution
        severity = Severity.HIGH 

    else:
        # If no known issue, use simple keyword matching (simulating LLM classification)
        text = description.lower()

        if "login" in text or "password" in text:
            category = Category.ACCOUNT
            severity = Severity.MEDIUM
            summary = "User unable to log in."
            suggested_action = "Ask user to try clearing cache or verify credentials."
        elif "charged" in text or "invoice" in text:
            category = Category.BILLING
            severity = Severity.MEDIUM
            summary = "Inquiry regarding billing or charges."
            suggested_action = "Escalate to Billing team for review."
        else:
            # Default fallback for new/unclassified issues
            category = Category.OTHER
            severity = Severity.LOW
            summary = "New general support request."
            suggested_action = "Support team will review and classify this new issue."
            
    # --- 3. Return Final Structured Result ---

    return TriageResult(
        summary=summary,
        category=category,
        severity=severity,
        is_known_issue=is_known_issue,
        related_kb_ids=related_kb_ids,
        suggested_action=suggested_action
    )