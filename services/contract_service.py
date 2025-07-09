
import requests
import logging
from config import ETHERSCAN_API_KEY
from services.solscan_service import fetch_solscan_token_info

logger = logging.getLogger(__name__)

def analyze_contract(contract_address: str):
    source_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    try:
        source_resp = requests.get(source_url, timeout=10).json()
    except Exception as e:
        logger.warning(f"Etherscan request failed: {e}")
        source_resp = {"status": "0"}

    if source_resp.get("status") != "1":
        logger.warning(f"Etherscan failed. Trying Solscan fallback for {contract_address}")
        solscan_data = fetch_solscan_token_info(contract_address)
        return {
            "is_verified": solscan_data.get("is_verified", False),
            "has_delegatecall": False,
            "has_selfdestruct": False,
            "holders_count": solscan_data.get("holder", None),
            "top_holder_ratio": None
        }

    try:
        source_data = source_resp["result"][0]
        is_verified = bool(source_data["SourceCode"])
        source_code = source_data["SourceCode"].lower()
        return {
            "is_verified": is_verified,
            "has_delegatecall": "delegatecall" in source_code,
            "has_selfdestruct": "selfdestruct" in source_code or "suicide" in source_code,
            "holders_count": None,
            "top_holder_ratio": None
        }
    except Exception as e:
        logger.error(f"Error parsing source code: {e}")
        return {
            "is_verified": False,
            "has_delegatecall": False,
            "has_selfdestruct": False,
            "holders_count": None,
            "top_holder_ratio": None
        }
    