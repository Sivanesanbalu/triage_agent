from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Category(str, Enum):
    BILLING = "Billing"
    LOGIN = "Login"
    PERFORMANCE = "Performance"
    BUG = "Bug"
    QUESTION = "Question/How-To"

class TicketInput(BaseModel):
    description: str = Field(..., min_length=5, description="The raw support ticket text")

class TriageResult(BaseModel):
    summary: str = Field(..., description="A 1-2 line summary of the issue")
    category: Category
    severity: Severity
    is_known_issue: bool = Field(..., description="True if similar to a KB item")
    related_kb_ids: List[str] = Field(default=[], description="IDs of related KB articles found")
    suggested_action: str = Field(..., description="The recommended next step")