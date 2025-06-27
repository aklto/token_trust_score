
from services.solana_token_service import fetch_token_metadata
from services.token_profile_builder import build_token_profile
from services.llm_analysis_service import analyze_trust_score_with_llm

def calculate_trust_score(token_id: str, contract_address: str) -> float:
    meta = fetch_token_metadata(contract_address)
    if not meta:
        return 0.0

    # Примерные заглушки под будущие данные
    tx_count = meta.get("tx_count_30d", 1200)
    recent_mints = meta.get("recent_mints", 0)
    recent_burns = meta.get("recent_burns", 0)

    profile = build_token_profile(meta, tx_count, recent_mints, recent_burns)
    llm_score = analyze_trust_score_with_llm(profile)

    # Вес LLM-анализа 100%, остальные метрики можно будет подключать позже
    return round(llm_score, 3)
