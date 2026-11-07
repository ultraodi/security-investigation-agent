from pydantic import BaseModel
from typing import Literal

class InvestigationReport(BaseModel):
    alert_summary: str
    evidence: list[str]
    analysis: str
    assessment: Literal[
        "malicious", "suspicious", "benign", "inconclusive"
    ]
    confidence: Literal["low", "medium", "high"]
    missing_information: list[str]
    recommended_next_steps: list[str]