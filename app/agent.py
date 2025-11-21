# app/agent.py

# Import schemas and the KB tool
from app.schemas import TriageResult, Category, Severity
from app.kb_tool import kb_tool # <-- Import the tool

def triage_ticket(description: str) -> TriageResult:
    known_issues = kb_tool.search(description)
    
    is_known_issue = len(known_issues) > 0
    related_kb_ids = [issue['id'] for issue in known_issues]
    
    if is_known_issue:
        top_issue = known_issues[0]
        suggested_action = top_issue['resolution']
        summary = f"Known issue: {top_issue['title']}"
        category_str = top_issue.get('category', 'OTHER').upper() 
        try:
            category = Category[category_str]
        except KeyError:
            category = Category.OTHER
          
        severity = Severity.HIGH 

    else:
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
            category = Category.OTHER
            severity = Severity.LOW
            summary = "New general support request."
            suggested_action = "Support team will review and classify this new issue."
            
    return TriageResult(
        summary=summary,
        category=category,
        severity=severity,
        is_known_issue=is_known_issue,
        related_kb_ids=related_kb_ids,
        suggested_action=suggested_action
    )