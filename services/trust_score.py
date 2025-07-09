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

def calculate_trust_score(token_id: str, contract_address: str, token_data: dict = None) -> float:
    from services.embedding_service import get_embedding
    from services.contract_service import analyze_contract

    contract_info = analyze_contract(contract_address)

    contract_safety_score = get_contract_safety_score(contract_info)
    holders_score = get_holders_score(contract_info)

    # fetch activity info from metadata (stubbed or real)
    meta = fetch_token_metadata(contract_address)
    tx_count = meta.get("tx_count_30d", 1200)
    mints = meta.get("recent_mints", 0)
    burns = meta.get("recent_burns", 0)
    activity_score = get_activity_score(tx_count, mints, burns)

    profile_parts = [
        f"Token Name: {token_data.get('name') if token_data else 'Unknown'}",
        f"Symbol: {token_data.get('symbol') if token_data else 'Unknown'}",
        f"Verified: {contract_info['is_verified']}",
        f"Holders: {contract_info['holders_count']}",
        f"Top Holder Owns: {contract_info['top_holder_ratio'] or 0.0}%",
    ]
    profile_text = "\n".join(profile_parts)

    llm_score = analyze_trust_score_with_llm(profile_text)
    embedding = get_embedding(
        token_data.get("name", "") + " " + token_data.get("description", "")) if token_data else []
    embedding_score = sum(embedding) / len(embedding) if embedding else 0.0

    final_score = (
        0.25 * contract_safety_score +
        0.15 * holders_score +
        0.15 * activity_score +
        0.2 * llm_score +
        0.25 * embedding_score
    )

    print(f"token: {token_id}")
    print("contract_safety_score:", contract_safety_score)
    print("holders_score:", holders_score)
    print("activity_score:", activity_score)
    print("llm_score:", llm_score)
    print("embedding_score:", embedding_score)

    return round(final_score, 3)
