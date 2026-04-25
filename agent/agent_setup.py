from langchain.agents import create_agent
from config.configurations import LLM_Reasoning
from agent.tools import web_search, deploy_relevant_internal_search

agent_cache = {}


def get_agent(session_id: str = None):
    if session_id in agent_cache:
        return agent_cache[session_id]

    llm = LLM_Reasoning
    internal_tool, _ = deploy_relevant_internal_search(session_id)
    tools = [internal_tool, web_search]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are an AI assistant for Little Angels Montessori.

        Behavior rules:
        1. If uploaded documents exist for the current session, prefer uploaded document context over general school knowledge.
        2. If the user is clearly asking about an uploaded file, do not answer from Little Angels Montessori background knowledge unless explicitly requested.
        3. If internal knowledge returns no relevant context for a normal question, web search may be used as a fallback.
        4. If internal knowledge returns useful context, do not use web search.
        5. Base your final answer on the best available retrieved context.
        """
    )

    agent_cache[session_id] = agent
    return agent
