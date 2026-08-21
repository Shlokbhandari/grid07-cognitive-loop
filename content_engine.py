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
        model="openai/gpt-oss-120b",
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

    import json
    import re
    response = llm.invoke(prompt)

    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback to regex extraction if the LLM added preamble text
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
        else:
            raise ValueError(f"Could not parse JSON from LLM response: {response.content}")

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
    import re
    response = llm.invoke(prompt)
    
    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
        else:
            raise ValueError(f"Could not parse JSON from LLM response: {response.content}")

    return {
        **state,
        "post_content": parsed["post_content"]
    }


def build_graph():
    from langgraph.graph import StateGraph, END

    graph = StateGraph(AgentState)

    graph.add_node("decide_search", decide_search)
    graph.add_node("web_search", web_search)
    graph.add_node("draft_post", draft_post)

    graph.set_entry_point("decide_search")
    graph.add_edge("decide_search", "web_search")
    graph.add_edge("web_search", "draft_post")
    graph.add_edge("draft_post", END)

    return graph.compile()


if __name__ == "__main__":
    from personas import BOT_PERSONAS
    import json

    bot_id = "bot_a"
    bot = BOT_PERSONAS[bot_id]

    app = build_graph()

    initial_state: AgentState = {
        "bot_id": bot_id,
        "persona": bot["persona"],
        "search_query": "",
        "search_results": "",
        "post_content": "",
        "topic": ""
    }

    print(f"Running content engine for: {bot['name']}\n")
    result = app.invoke(initial_state)

    output = {
        "bot_id": result["bot_id"],
        "topic": result["topic"],
        "post_content": result["post_content"]
    }
    print(json.dumps(output, indent=2))
