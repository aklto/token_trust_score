
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_token_market_data(token_id: str) -> dict:
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{token_id.lower()}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            market_data = {
                "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd"),
                "volume_24h": data.get("market_data", {}).get("total_volume", {}).get("usd"),
                "description": data.get("description", {}).get("en", ""),
                "symbol": data.get("symbol", ""),
                "name": data.get("name", "")
            }
            return market_data
        else:
            logger.warning(f"⚠️ Token '{token_id}' not found on CoinGecko.")
            return {}
    except Exception as e:
        logger.error(f"❌ CoinGecko API error: {e}")
        return {}
    