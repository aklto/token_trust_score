from services.solana_token_service import fetch_token_metadata
from services.token_profile_builder import build_token_profile
from services.llm_analysis_service import analyze_trust_score_with_llm
from services.embedding_similarity import calculate_embedding_similarity
from services.contract_service import analyze_contract

def get_contract_safety_score(data):
    if not data.get("is_verified", False):
        return 0.0
    if data.get("has_delegatecall") or data.get("has_selfdestruct"):
        return 0.2
    return 1.0


def get_holders_score(contract_data: dict) -> float:
    ratio = contract_data.get("top_holder_ratio")

    if ratio is None:
        return 0.5

    if ratio >= 0.9:
        return 0.0
    elif ratio >= 0.5:
        return 0.3
    else:
        return 1.0


def get_activity_score(tx_count, mints, burns):
    total = tx_count + mints + burns
    if total > 5000: return 1.0
    if total > 1000: return 0.7
    if total > 100: return 0.4
    return 0.1

def calculate_trust_score(token_id: str, contract_address: str) -> float:
    meta = fetch_token_metadata(contract_address)
    if not meta:
        return 0.0

    contract_data = analyze_contract(contract_address)
    tx_count = meta.get("tx_count_30d", 1200)
    recent_mints = meta.get("recent_mints", 0)
    recent_burns = meta.get("recent_burns", 0)

    profile = build_token_profile(meta, tx_count, recent_mints, recent_burns)
    llm_score = analyze_trust_score_with_llm(profile)
    embedding_score = calculate_embedding_similarity(f"{meta.get('name', '')} {meta.get('description', '')}")
    contract_safety_score = get_contract_safety_score(contract_data)
    holders_score = get_holders_score(contract_data)
    activity_score = get_activity_score(tx_count, recent_mints, recent_burns)

    final_score = (
        0.4 * llm_score +
        0.2 * embedding_score +
        0.2 * contract_safety_score +
        0.1 * holders_score +
        0.1 * activity_score
    )
    return round(final_score, 3)
