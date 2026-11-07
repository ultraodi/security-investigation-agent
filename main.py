from agents.investigation_agent import investigation_agent
from agents.response_agent import response_agent


def main():
    content = (
        "Investigate this suspicious API request. "
        "Request ID: req-001. "
        "The gateway detected repeated failed authentication "
        "attempts. If you need more information, say so."
    )

    print("Running security investigation...\n", flush=True)

    investigation_result = investigation_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": content}
            ]
        },
        config={"configurable": {"thread_id": "investigation-req-001"}},
    )

    print("\nInvestigation Report:\n")

    print(investigation_result["messages"][-1].content)


    print("Running Response plan...\n", flush=True)

    response_result = response_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": content}
            ]
        },
        config={"configurable": {"thread_id": "investigation-req-001"}},
    )

    print("\nResponse Report:\n")

    print(response_result["messages"][-1].content)



if __name__ == "__main__":
    main()
