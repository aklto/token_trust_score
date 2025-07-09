
import httpx
import logging

logger = logging.getLogger(__name__)
SOLSCAN_BASE_URL = "https://public-api.solscan.io"

def fetch_solscan_token_info(contract_address: str) -> dict:
    try:
        url = f"{SOLSCAN_BASE_URL}/token/meta?tokenAddress={contract_address}"
        headers = {"accept": "application/json"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if response.status_code == 404:
            logger.info(f"🔎 Token not found on Solscan: {contract_address}")
            return {}
        return response.json()
    except Exception as e:
        logger.error(f"❌ Solscan API error: {e}")
        return {}
    