import requests
import logging
from config import ETHERSCAN_API_KEY

logger = logging.getLogger(__name__)

def analyze_contract(contract_address: str):
    source_url = (
        f"https://api.etherscan.io/api?module=contract&action=getsourcecode"
        f"&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    )
    source_resp = requests.get(source_url).json()

    try:
        source_data = source_resp['result'][0]
        is_verified = source_data['SourceCode'] != ''
        source_code = source_data['SourceCode']
        has_delegatecall = 'delegatecall' in source_code.lower()
        has_selfdestruct = 'selfdestruct' in source_code.lower() or 'suicide' in source_code.lower()
    except Exception as e:
        logger.error(f"Error parsing source code data: {e}")
        is_verified = False
        has_delegatecall = False
        has_selfdestruct = False

    holders_count = None
    top_holder_ratio = None

    try:
        holders_url = (
            f"https://api.etherscan.io/api?module=token&action=tokenholderlist"
            f"&contractaddress={contract_address}&page=1&offset=10&apikey={ETHERSCAN_API_KEY}"
        )
        holders_resp = requests.get(holders_url).json()
        print("🔍 Raw holders_resp:", holders_resp)

        result = holders_resp.get("result", [])
        if isinstance(result, list):
            total_top = sum(int(h['TokenHolderQuantity'].split('.')[0]) for h in result)
            holders_count = len(result)
            top_holder_ratio = (
                int(result[0]['TokenHolderQuantity'].split('.')[0]) / total_top
                if total_top > 0 else 0.0
            )
        else:
            logger.warning("⚠️ holders_resp['result'] is not a list")
    except Exception as e:
        logger.error(f"Error parsing holders data: {e}")
        holders_count = 0
        top_holder_ratio = 1.0

    return {
        "is_verified": is_verified,
        "has_delegatecall": has_delegatecall,
        "has_selfdestruct": has_selfdestruct,
        "holders_count": holders_count,
        "top_holder_ratio": top_holder_ratio
    }
