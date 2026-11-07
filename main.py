from workflow.graph import workflow

def main():
    content = (
        "Investigate this suspicious API request. "
        "Request ID: req-001. "
        "The gateway detected repeated failed authentication "
        "attempts. If you need more information, say so."
    )

    result = workflow.invoke({
        "alert": content,
        "investigation_report": None,
        "response_plan": None,
    })

    print(result["response_plan"].model_dump_json(indent=4))


if __name__ == "__main__":
    main()
