
def calculate_final_score(
    contract_safety_score: float | None,
    holders_score: float | None,
    activity_score: float | None,
    llm_score: float | None,
    embedding_score: float | None
) -> float:
    weights = {
        "contract_safety_score": 0.2,
        "holders_score": 0.2,
        "activity_score": 0.2,
        "llm_score": 0.2,
        "embedding_score": 0.2
    }

    scores = {
        "contract_safety_score": contract_safety_score,
        "holders_score": holders_score,
        "activity_score": activity_score,
        "llm_score": llm_score,
        "embedding_score": embedding_score
    }

    # Убираем недоступные
    available_scores = {k: v for k, v in scores.items() if v is not None}
    total_weight = sum([weights[k] for k in available_scores.keys()])

    if total_weight == 0:
        return 0.0


    adjusted_weights = {k: weights[k] / total_weight for k in available_scores.keys()}

    final_score = sum(adjusted_weights[k] * available_scores[k] for k in available_scores)

    return round(final_score, 3)
