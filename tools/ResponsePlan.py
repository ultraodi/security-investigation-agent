from pydantic import BaseModel

class ResponsePlan(BaseModel):
    risk_summary: str
    recommended_actions: list[str]
    approval_required: str
    additional_information_needed: list[str]