from langgraph.graph import START, END, StateGraph

from workflow.state import InvestigationState
from agents.investigation_agent import investigation_agent
from agents.response_agent import response_agent


def investigation_node(state: InvestigationState):
    result = investigation_agent.invoke({
        "messages": [
            {"role": "user", "content": state["alert"]}
        ]
    })

    return {
        "investigation_report": result["structured_response"]
    }


def response_node(state: InvestigationState):
    result = response_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": state["investigation_report"].model_dump_json()
            }
        ]
    })

    return {
        "response_plan": result["structured_response"]
    }


builder = StateGraph(InvestigationState)

builder.add_node("investigation_node", investigation_node)
builder.add_node("response_node", response_node)

builder.add_edge(START, "investigation_node")
builder.add_edge("investigation_node", "response_node")
builder.add_edge("response_node", END)

workflow = builder.compile()