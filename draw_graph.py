from email_assistant import build_email_agent


def main():
    email_agent = build_email_agent()
    graph = email_agent.get_graph(xray=True)

    # Always works, no network needed
    print(graph.draw_ascii())

    # Mermaid source, viewable at https://mermaid.live or in any Markdown renderer
    with open("graph.mmd", "w", encoding="utf-8") as f:
        f.write(graph.draw_mermaid())
    print("Wrote graph.mmd")

    # PNG render (calls the hosted mermaid.ink API, needs internet access)
    try:
        with open("graph.png", "wb") as f:
            f.write(graph.draw_mermaid_png())
        print("Wrote graph.png")
    except Exception as e:
        print(f"Skipped graph.png ({e}); graph.mmd / ASCII above still available")


if __name__ == "__main__":
    main()
