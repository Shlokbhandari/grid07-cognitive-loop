from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from personas import BOT_PERSONAS


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def build_persona_store():
    """Embed all bot personas and store them in FAISS."""
    embeddings = get_embedding_model()

    texts = []
    metadatas = []
    for bot_id, bot_data in BOT_PERSONAS.items():
        texts.append(bot_data["persona"])
        metadatas.append({"bot_id": bot_id, "name": bot_data["name"]})

    store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return store


if __name__ == "__main__":
    print("Building persona vector store...")
    store = build_persona_store()
    print(f"Stored {len(BOT_PERSONAS)} bot personas in FAISS")

    # quick sanity check
    results = store.similarity_search_with_score("AI is the future", k=3)
    for doc, score in results:
        print(f"  {doc.metadata['name']}: {score:.4f}")