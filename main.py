from email_assistant import build_email_agent

config = {"configurable": {"langgraph_user_id": "lance"}}


def print_messages(response):
    for m in response["messages"]:
        m.pretty_print()


def main():
    email_agent = build_email_agent()

    email_input = {
        "author": "Alice Smith <alice.smith@company.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John,

I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

Specifically, I'm looking at:
- /auth/refresh
- /auth/validate

Thanks!
Alice""",
    }

    response = email_agent.invoke({"email_input": email_input}, config=config)
    print_messages(response)

    follow_up = {
        "author": "Alice Smith <alice.smith@company.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Follow up",
        "email_thread": "Hi John,\n\nAny update on my previous ask?",
    }

    response = email_agent.invoke({"email_input": follow_up}, config=config)
    print_messages(response)


if __name__ == "__main__":
    main()
