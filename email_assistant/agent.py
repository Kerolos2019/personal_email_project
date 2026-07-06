from langgraph.prebuilt import create_react_agent
from langgraph.store.base import BaseStore

from email_assistant.config import RESPONSE_MODEL, profile, prompt_instructions
from email_assistant.memory import build_memory_tools
from email_assistant.prompts import agent_system_prompt_memory
from email_assistant.tools import check_calendar_availability, schedule_meeting, write_email


def create_prompt(state):
    return [
        {
            "role": "system",
            "content": agent_system_prompt_memory.format(
                instructions=prompt_instructions["agent_instructions"],
                profile=profile,
                **profile,
            ),
        }
    ] + state["messages"]


def build_response_agent(store: BaseStore):
    manage_memory_tool, search_memory_tool = build_memory_tools()

    tools = [
        write_email,
        schedule_meeting,
        check_calendar_availability,
        manage_memory_tool,
        search_memory_tool,
    ]

    return create_react_agent(
        RESPONSE_MODEL,
        tools=tools,
        prompt=create_prompt,
        # Use this to ensure the store is passed to the agent
        store=store,
    )
