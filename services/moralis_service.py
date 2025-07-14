import httpx
import os
import logging

logger = logging.getLogger(__name__)
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

def fetch_moralis_holders(contract_address: str):
    try:
        url = f"https://deep-index.moralis.io/api/v2.2/erc20/{contract_address}/holders"
        headers = {
            "accept": "application/json",
            "X-API-Key": MORALIS_API_KEY,
        }
        params = {"page_size": 100}
        response = httpx.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        total_holders = data.get("totalHolders", 0)
        top_10_percent = data.get("holderSupply", {}).get("top10", {}).get("supplyPercent", 0)

        if total_holders > 0:
            top_holder_ratio = float(top_10_percent) / 100
            return total_holders, round(top_holder_ratio, 3)

        logger.warning(f"Moralis holders = 0 for {contract_address}")
        return 0, 0.0

    except Exception as e:
        logger.error(f"❌ Moralis API error: {e}")
        return None
