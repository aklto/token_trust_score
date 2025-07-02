from services.embedding_service import get_embedding
from services.solana_token_service import fetch_token_metadata
import numpy as np

IDEAL_TOKEN_ADDRESS = "5c74v6Px9RKwdGWCfqLGfEk7UZfE3Y4qJbuYrLbVG63V"

ideal_meta = fetch_token_metadata(IDEAL_TOKEN_ADDRESS)
ideal_text = f"{ideal_meta.get('name', '')} {ideal_meta.get('description', '')}" if ideal_meta else ""

ideal_embedding = get_embedding(ideal_text)

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def calculate_embedding_similarity(token_text: str) -> float:
    try:
        token_embedding = get_embedding(token_text)
        similarity = cosine_similarity(token_embedding, ideal_embedding)
        return similarity
    except Exception as e:
        print(f"Embedding similarity failed: {e}")
        return 0.0
