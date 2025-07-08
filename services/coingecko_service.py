import requests
import logging

logger = logging.getLogger(__name__)

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

def get_token_data(token_id: str) -> dict:
    url = f"{COINGECKO_BASE_URL}/coins/{token_id}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            logger.warning(f"⚠️ Token '{token_id}' not found on CoinGecko.")
            return {}
        else:
            logger.error(f"❌ Unexpected CoinGecko response: {resp.status_code} — {resp.text}")
            return {}
    except Exception as e:
        logger.error(f"❌ CoinGecko request failed: {e}")
        return {}

def fetch_market_data(token_id: str) -> dict:
    """
    Получает краткие данные о цене токена (если нужно отдельно).
    """
    url = f"{COINGECKO_BASE_URL}/simple/price?ids={token_id}&vs_currencies=usd"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            logger.warning(f"⚠️ Simple price fetch failed: {resp.status_code}")
            return {}
    except Exception as e:
        logger.error(f"❌ CoinGecko market fetch failed: {e}")
        return {}
