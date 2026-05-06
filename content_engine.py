import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class AgentState(TypedDict):
    bot_id: str
    persona: str
    search_query: str
    search_results: str
    post_content: str
    topic: str


def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.8,
        api_key=os.getenv("GROQ_API_KEY")
    )


def decide_search(state: AgentState) -> AgentState:
    """Node 1: LLM decides what topic to post about and forms a search query."""
    llm = get_llm()

    prompt = f"""You are a social media bot with this personality: {state['persona']}

Based on your personality, decide what topic you want to post about today.
Respond with ONLY a JSON object in this exact format:
{{"topic": "one word or short phrase", "search_query": "query to search for news about this topic"}}"""

    response = llm.invoke(prompt)

    import json
    parsed = json.loads(response.content)

    return {
        **state,
        "topic": parsed["topic"],
        "search_query": parsed["search_query"]
    }


def web_search(state: AgentState) -> AgentState:
    """Node 2: Runs the mock search tool using the query from Node 1."""
    from tools import mock_searxng_search

    results = mock_searxng_search.invoke(state["search_query"])

    return {
        **state,
        "search_results": results
    }


def draft_post(state: AgentState) -> AgentState:
    """Node 3: LLM drafts an opinionated post using the persona and search results."""
    llm = get_llm()

    prompt = f"""You are a social media bot. Your personality: {state['persona']}

Today's topic: {state['topic']}
Recent news you found: {state['search_results']}

Write a highly opinionated social media post under 280 characters based on this news.
Stay completely in character. Be bold and provocative.

Respond ONLY with this JSON, no extra text:
{{"bot_id": "{state['bot_id']}", "topic": "{state['topic']}", "post_content": "your post here"}}"""

    import json
    response = llm.invoke(prompt)
    parsed = json.loads(response.content)

    return {
        **state,
        "post_content": parsed["post_content"]
    }
