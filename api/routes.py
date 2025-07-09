import logging
from fastapi import APIRouter, HTTPException
from models.request_models import TokenRequest
from services.coingecko_service import fetch_token_market_data
from services.contract_service import analyze_contract
from services.embedding_service import get_embedding
from services.trust_score import calculate_trust_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/trust-score")
def get_trust_score(req: TokenRequest):
    logger.info(f"Incoming request: {req.dict()}")

    try:
        token_data = fetch_token_market_data(req.token_id)  # ✅ исправлено здесь
        logger.info(f"Token data fetched for {req.token_id}")

        contract_data = analyze_contract(req.contract_address)
        logger.info(f"Contract analysis completed for {req.contract_address}")

        score = calculate_trust_score(
            token_id=req.token_id,
            contract_address=req.contract_address,
            token_data=token_data  # 💡 возможно тебе пригодится здесь
        )

        response = {
            "token_id": req.token_id,
            "trust_score": round(score, 3),
            "contract_analysis": contract_data
        }

        logger.info(f"Final response: {response}")
        return response

    except Exception as e:
        logger.exception(f"Error while processing token {req.token_id}")
        raise HTTPException(status_code=400, detail=str(e))
