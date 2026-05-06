# Grid07 — Cognitive Routing & RAG

AI cognitive loop for the Grid07 platform. Uses LangGraph for LLM orchestration, FAISS for vector-based persona matching, and RAG for contextual bot responses.

## Tech Stack

- **Python 3.10+**
- **LangChain / LangGraph** — LLM orchestration
- **FAISS** — Vector similarity search
- **Groq API (LLaMA 3.3 70B)** — LLM inference
- **Sentence Transformers** — Text embeddings

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your Groq API key
```

## Project Structure

```
├── personas.py          # Bot persona definitions
├── vector_store.py      # FAISS vector store setup
├── router.py            # Phase 1 — Post-to-bot routing
├── tools.py             # Mock search tool
├── content_engine.py    # Phase 2 — LangGraph content generator
├── combat_engine.py     # Phase 3 — Thread-aware reply engine
├── main.py              # Run all phases
├── requirements.txt
├── .env.example
└── README.md
```

## Phases

### Phase 1: Vector-Based Persona Matching

Each bot persona is embedded using `all-MiniLM-L6-v2` and stored in a FAISS in-memory vector store. When a new post arrives, it gets embedded and compared against all persona vectors using cosine similarity.

```python
route_post_to_bots("OpenAI just released a new model that might replace junior developers.")
# → ['bot_a']  (Tech Maximalist matched, threshold = -0.25)
```

The threshold was tuned based on actual similarity scores produced by the embedding model. FAISS returns L2 distances which are converted to cosine similarity using: `cosine_sim = 1 - (l2_dist² / 2)`.

### Phase 2: Autonomous Content Engine (LangGraph)
*Coming soon...*

### Phase 3: Combat Engine with Prompt Injection Defense
*Coming soon...*
