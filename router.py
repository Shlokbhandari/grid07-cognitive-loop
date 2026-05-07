from vector_store import build_persona_store, get_embedding_model

vector_store = build_persona_store()

def route_post_to_bots(post_content: str, threshold: float = 0.50) -> list[str]:
    # Query FAISS (returns L2 distance)
    results = vector_store.similarity_search_with_score(post_content, k=3)
    matching_bots = []
    
    print(f"\nAnalyzing Post: '{post_content}'")
    
    for doc, l2_dist in results:
        bot_id = doc.metadata["bot_id"]
        bot_name = doc.metadata["name"]
        
        # Convert squared L2 distance to Cosine Similarity accurately
        # FAISS returns squared L2 distance by default
        cosine_sim = 1.0 - (l2_dist / 2.0)
        
        print(f"  - [{bot_name}] Cosine Similarity: {cosine_sim:.4f}")
        
        if cosine_sim >= threshold:
            matching_bots.append(bot_id)
            
    return matching_bots

if __name__ == "__main__":
    post_1 = "OpenAI just released a new model that might replace junior developers."
    matched_1 = route_post_to_bots(post_1, threshold=0.20)
    print(f"Bots notified: {matched_1}")
    print("-" * 40)
    
    post_2 = "The Federal Reserve just announced a 50 basis point interest rate cut. Markets are rallying."
    matched_2 = route_post_to_bots(post_2, threshold=0.20)
    print(f"Bots notified: {matched_2}")
