import os

from dotenv import load_dotenv

load_dotenv()

TRIAGE_MODEL = os.getenv("TRIAGE_MODEL", "openai:gpt-4o-mini")
RESPONSE_MODEL = os.getenv("RESPONSE_MODEL", "openai:gpt-4o")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "openai:text-embedding-3-small")

profile = {
    "name": "John",
    "full_name": "John Doe",
    "user_profile_background": "Senior software engineer leading a team of 5 developers",
}

prompt_instructions = {
    "triage_rules": {
        "ignore": "Marketing newsletters, spam emails, mass company announcements",
        "notify": "Team member out sick, build system notifications, project status updates",
        "respond": "Direct questions from team members, meeting requests, critical bug reports",
    },
    "agent_instructions": "Use these tools when appropriate to help manage John's tasks efficiently.",
}
