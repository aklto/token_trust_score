import random
from cachetools import TTLCache

from services.solana_token_service import fetch_token_metadata
from services.token_profile_builder import build_token_profile
from services.llm_analysis_service import analyze_trust_score_with_llm
from services.embedding_similarity import calculate_embedding_similarity
from services.contract_service import analyze_contract

trust_score_cache = TTLCache(maxsize=100, ttl=600)

def get_contract_safety_score(data):
    if not data.get("is_verified", False):
        return 0.0
    if data.get("has_delegatecall") or data.get("has_selfdestruct"):
        return 0.2
    return 1.0

def get_holders_score(contract_data: dict) -> float:
    ratio = contract_data.get("top_holder_ratio")
    if ratio is None:
        return 0.0
    if ratio >= 0.9:
        return 0.0
    elif ratio >= 0.5:
        return 0.3
    else:
        return 1.0

def get_activity_score(tx_count, mints, burns):
    if tx_count is None:
        return 0.0
    total = tx_count + mints + burns
    if total > 5000: return 1.0
    if total > 1000: return 0.7
    if total > 100: return 0.4
    return 0.1

def calculate_trust_score(token_id: str, contract_address: str, token_data: dict = None) -> float:
    from services.embedding_service import get_embedding

    cache_key = f"{token_id.lower()}_{contract_address.lower()}"
    if cache_key in trust_score_cache:
        return trust_score_cache[cache_key]

    contract_info = analyze_contract(contract_address)
    scores = {}
    weights = {}

    contract_safety_score = get_contract_safety_score(contract_info)
    if contract_safety_score > 0.0:
        scores["contract_safety"] = contract_safety_score
        weights["contract_safety"] = 0.25

    holders_score = get_holders_score(contract_info)
    if holders_score > 0.0:
        scores["holders"] = holders_score
        weights["holders"] = 0.15

    meta = fetch_token_metadata(contract_address)
    tx_count = meta.get("tx_count_30d")
    mints = meta.get("recent_mints", 0)
    burns = meta.get("recent_burns", 0)
    activity_score = get_activity_score(tx_count, mints, burns)
    if activity_score > 0.0:
        scores["activity"] = activity_score
        weights["activity"] = 0.15

    profile_text = f"Token ID: {token_id}\nAddress: {contract_address}"
    llm_score = analyze_trust_score_with_llm(profile_text)
    if llm_score > 0.0:
        scores["llm"] = llm_score
        weights["llm"] = 0.25

    if token_data:
        embedding = get_embedding(
            token_data.get("name", "") + " " + token_data.get("description", "")
        )
        embedding_score = max(0.0, sum(embedding) / len(embedding)) if embedding else 0.0
        if embedding_score > 0.0:
            scores["embedding"] = embedding_score
            weights["embedding"] = 0.2

    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    final_score = sum(
        scores[k] * (weights[k] / total_weight) for k in scores
    )

    jitter = random.uniform(-0.03, 0.03)
    final_score = max(0.0, min(1.0, final_score + jitter))

    print(f"token: {token_id}")
    for k in scores:
        print(f"{k}_score: {scores[k]} (weight: {weights[k]})")
    print("final_score (normalized + jitter):", round(final_score, 3))

    final_score = round(final_score, 3)
    trust_score_cache[cache_key] = final_score
    return final_score
