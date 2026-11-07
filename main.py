from agents.investigation_agent import investigation_agent


def main():
    content = (
        "Investigate this suspicious API request. "
        "Request ID: req-001. "
        "The gateway detected repeated failed authentication "
        "attempts. If you need more information, say so."
    )

    print("Running security investigation...\n", flush=True)

    result = investigation_agent.invoke(
        {
            "messages": [
                {"role": "user", "content": content}
            ]
        },
        config={"configurable": {"thread_id": "investigation-req-001"}},
    )

    print("\nInvestigation Report:\n")

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
