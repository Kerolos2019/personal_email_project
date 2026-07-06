from typing import Literal

from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from email_assistant.agent import build_response_agent
from email_assistant.config import TRIAGE_MODEL, profile, prompt_instructions
from email_assistant.memory import build_store
from email_assistant.prompts import triage_system_prompt, triage_user_prompt
from email_assistant.schemas import Router, State

llm_router = init_chat_model(TRIAGE_MODEL).with_structured_output(Router)


def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:
    author = state["email_input"]["author"]
    to = state["email_input"]["to"]
    subject = state["email_input"]["subject"]
    email_thread = state["email_input"]["email_thread"]

    system_prompt = triage_system_prompt.format(
        full_name=profile["full_name"],
        name=profile["name"],
        user_profile_background=profile["user_profile_background"],
        triage_no=prompt_instructions["triage_rules"]["ignore"],
        triage_notify=prompt_instructions["triage_rules"]["notify"],
        triage_email=prompt_instructions["triage_rules"]["respond"],
        examples=None,
    )
    user_prompt = triage_user_prompt.format(
        author=author,
        to=to,
        subject=subject,
        email_thread=email_thread,
    )
    result = llm_router.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        goto = "response_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Respond to the email {state['email_input']}",
                }
            ]
        }
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
        update = None
        goto = END
    elif result.classification == "notify":
        # If real life, this would do something else
        print("🔔 Classification: NOTIFY - This email contains important information")
        update = None
        goto = END
    else:
        raise ValueError(f"Invalid classification: {result.classification}")

    return Command(goto=goto, update=update)


def build_email_agent():
    store = build_store()
    response_agent = build_response_agent(store)

    workflow = StateGraph(State)
    workflow.add_node(triage_router)
    workflow.add_node("response_agent", response_agent)
    workflow.add_edge(START, "triage_router")

    return workflow.compile(store=store)
