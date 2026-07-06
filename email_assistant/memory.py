from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool

from email_assistant.config import EMBEDDING_MODEL

MEMORY_NAMESPACE = ("email_assistant", "{langgraph_user_id}", "collection")


def build_store() -> InMemoryStore:
    return InMemoryStore(index={"embed": EMBEDDING_MODEL})


def build_memory_tools(namespace: tuple = MEMORY_NAMESPACE):
    manage_memory_tool = create_manage_memory_tool(namespace=namespace)
    search_memory_tool = create_search_memory_tool(namespace=namespace)
    return manage_memory_tool, search_memory_tool
