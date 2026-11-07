from typing_extensions import TypedDict
from agents.investigation_agent import InvestigationReport
from agents.response_agent import ResponsePlan


class InvestigationState(TypedDict):
    alert: str
    investigation_report: InvestigationReport | None
    response_plan: ResponsePlan | None