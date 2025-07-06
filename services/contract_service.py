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

    if source_resp.get('status') != '1':
        logger.error(f"Etherscan source error: {source_resp.get('message')} - {source_resp.get('result')}")
        return {
            "is_verified": False,
            "has_delegatecall": False,
            "has_selfdestruct": False,
            "holders_count": 0,
            "top_holder_ratio": 1.0
        }

    try:
        source_data = source_resp['result'][0]
        is_verified = source_data['SourceCode'] != ''
        source_code = source_data['SourceCode']
        has_delegatecall = 'delegatecall' in source_code.lower()
        has_selfdestruct = 'selfdestruct' in source_code.lower() or 'suicide' in source_code.lower()
    except (IndexError, KeyError, TypeError) as e:
        logger.error(f"Error parsing source code data: {e}")
        is_verified = False
        has_delegatecall = False
        has_selfdestruct = False

    holders_url = (
        f"https://api.etherscan.io/api?module=token&action=tokenholderlist"
        f"&contractaddress={contract_address}&page=1&offset=10&apikey={ETHERSCAN_API_KEY}"
    )
    holders_resp = requests.get(holders_url).json()

    try:
        top_holders = holders_resp['result']
        total_top = sum(int(h['TokenHolderQuantity'].split('.')[0]) for h in top_holders)
        holders_count = len(top_holders)
        top_holder_ratio = (
            int(top_holders[0]['TokenHolderQuantity'].split('.')[0]) / total_top
            if total_top > 0 else 0.0
        )
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
