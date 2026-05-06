from langchain_core.tools import tool


@tool
def mock_searxng_search(query: str) -> str:
    """Search for recent news headlines based on a query."""
    query_lower = query.lower()

    if "crypto" in query_lower or "bitcoin" in query_lower:
        return "Bitcoin hits new all-time high amid regulatory ETF approvals. Ethereum follows with 20% weekly gains."

    if "ai" in query_lower or "openai" in query_lower or "llm" in query_lower:
        return "OpenAI's GPT-5 reportedly outperforms all benchmarks. Tech companies racing to integrate AI agents into core products."

    if "market" in query_lower or "stock" in query_lower or "fed" in query_lower or "interest rate" in query_lower:
        return "Fed signals potential rate cuts as inflation cools. S&P 500 reaches record high on positive jobs data."

    if "elon" in query_lower or "tesla" in query_lower or "spacex" in query_lower:
        return "SpaceX Starship completes successful orbital test. Elon Musk announces new Mars mission timeline for 2028."

    if "climate" in query_lower or "environment" in query_lower or "nature" in query_lower:
        return "UN report warns of accelerating biodiversity loss. Activists push for stricter corporate emissions regulations."

    return "Global tech spending projected to exceed $5 trillion in 2025. AI and cloud infrastructure lead growth sectors."
