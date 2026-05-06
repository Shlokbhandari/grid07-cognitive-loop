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
