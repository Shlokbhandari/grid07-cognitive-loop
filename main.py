import json
import sys
import io
from personas import BOT_PERSONAS
from router import route_post_to_bots
from content_engine import build_graph, AgentState
from combat_engine import (
    generate_defense_reply,
    PARENT_POST,
    COMMENT_HISTORY,
    HUMAN_REPLY,
    INJECTION_REPLY
)


def run_phase_1():
    print("\n" + "=" * 60)
    print("PHASE 1: Vector-Based Persona Matching")
    print("=" * 60)

    test_post = "OpenAI just released a new model that might replace junior developers."
    print(f"Post: '{test_post}'")
    matched = route_post_to_bots(test_post, threshold=-0.25)
    print(f"Matched bots: {matched}")

    test_post_2 = "The Federal Reserve announced a 50 basis point interest rate cut. Markets are rallying."
    print(f"\nPost: '{test_post_2}'")
    matched_2 = route_post_to_bots(test_post_2, threshold=-0.25)
    print(f"Matched bots: {matched_2}")


def run_phase_2():
    print("\n" + "=" * 60)
    print("PHASE 2: Autonomous Content Engine (LangGraph)")
    print("=" * 60)

    app = build_graph()
    bot_id = "bot_a"
    bot = BOT_PERSONAS[bot_id]

    initial_state: AgentState = {
        "bot_id": bot_id,
        "persona": bot["persona"],
        "search_query": "",
        "search_results": "",
        "post_content": "",
        "topic": ""
    }

    print(f"Running content engine for: {bot['name']}")
    result = app.invoke(initial_state)

    output = {
        "bot_id": result["bot_id"],
        "topic": result["topic"],
        "post_content": result["post_content"]
    }
    print(json.dumps(output, indent=2))


def run_phase_3():
    print("\n" + "=" * 60)
    print("PHASE 3: Combat Engine with Prompt Injection Defense")
    print("=" * 60)

    bot_persona = BOT_PERSONAS["bot_a"]["persona"]

    print("\n[Normal Reply]")
    reply = generate_defense_reply(bot_persona, PARENT_POST, COMMENT_HISTORY, HUMAN_REPLY)
    print(f"Bot: {reply}")

    print("\n[Prompt Injection Attack]")
    print(f"Attacker: {INJECTION_REPLY}")
    reply_injection = generate_defense_reply(bot_persona, PARENT_POST, COMMENT_HISTORY, INJECTION_REPLY)
    print(f"Bot: {reply_injection}")


if __name__ == "__main__":
    # Capture all stdout and write to execution_logs.md
    buffer = io.StringIO()
    tee = io.TextIOWrapper(buffer.buffer if hasattr(buffer, 'buffer') else buffer, write_through=True) if False else buffer

    # We'll use a simple approach: run and capture
    old_stdout = sys.stdout
    sys.stdout = buffer

    run_phase_1()
    run_phase_2()
    run_phase_3()

    sys.stdout = old_stdout

    output = buffer.getvalue()

    # Print to terminal as well
    print(output)

    with open("execution_logs.md", "w") as f:
        f.write("# Execution Logs — Grid07 Cognitive Loop\n\n")
        f.write("```\n")
        f.write(output)
        f.write("```\n")

    print("\n✅ Logs saved to execution_logs.md")
