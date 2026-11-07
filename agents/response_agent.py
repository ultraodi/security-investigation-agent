from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from tools.ResponsePlan import ResponsePlan

RESPONSE_SYSTEM_PROMPT = """
You are a Security Response Planning Agent.

## Objective

Analyze security investigation reports and produce
a practical response plan based on the findings.

## Responsibilities

1. Review the investigation report.
2. Identify the security risks and their potential impact.
3. Determine which actions should be prioritized.
4. Explain the reasoning behind each recommended action.
5. Identify actions that require human approval.

## Rules

- Base recommendations on the investigation report.
- Do not invent evidence or assume that an attack was successful.
- Distinguish confirmed findings from potential risks.
- Do not recommend blocking or disrupting services without
  considering the potential operational impact.
- If information is insufficient, identify what is missing.
- Prioritize actions according to severity and urgency.
- You are strictly advisory and read-only.
- Never execute security actions or modify infrastructure.

## Output

Produce a response plan containing:

1. Overall risk summary.
2. Recommended actions, ordered by priority.
3. Reasoning for each action.
4. Potential operational impact.
5. Actions requiring human approval.
6. Additional information needed, if any.
"""

checkpointer = InMemorySaver()

model = init_chat_model(
    "openai:gpt-5.5",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

response_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=RESPONSE_SYSTEM_PROMPT,
    response_format=ResponsePlan,
    checkpointer=checkpointer,
)