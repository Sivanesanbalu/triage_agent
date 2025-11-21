from pydantic import BaseModel
from enum import Enum
from typing import List

class Category(str, Enum):
    BUG = "Bug"
    BILLING = "Billing"
    LOGIN = "Login"          
    PERFORMANCE = "Performance" 
    QUESTION = "Question/How-To"
    ACCOUNT = "Account"
    OTHER = "Other"

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TicketInput(BaseModel):
    description: str

class TriageResult(BaseModel):
    summary: str
    category: Category
    severity: Severity
    is_known_issue: bool
    related_kb_ids: List[str] = []
    suggested_action: str
