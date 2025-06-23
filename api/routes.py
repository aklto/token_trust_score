from fastapi import APIRouter, HTTPException
from models.request_models import TokenRequest
from services.coingecko_service import get_token_data
from services.github_service import get_repo_data
from services.contract_service import analyze_contract
from services.embedding_service import get_embedding
from services.trust_score import calculate_trust_score

router = APIRouter()

@router.post("/trust-score")
def get_trust_score(req: TokenRequest):
    try:
        token_data = get_token_data(req.token_id)
        repo_data = get_repo_data(req.github_repo)
        contract_data = analyze_contract(req.contract_address)

        text = f"{repo_data['description']}\n{repo_data['readme']}\nStars: {repo_data['stars']} Forks: {repo_data['forks']}"
        embedding = get_embedding(text)

        score = calculate_trust_score(token_data, repo_data, contract_data, embedding)

        return {
            "token_id": req.token_id,
            "trust_score": round(score, 3),
            "contract_analysis": contract_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
