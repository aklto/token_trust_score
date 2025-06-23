import requests
from config import ETHERSCAN_API_KEY

def analyze_contract(contract_address: str):
    source_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    source_resp = requests.get(source_url).json()
    is_verified = source_resp['result'][0]['SourceCode'] != ''
    source_code = source_resp['result'][0]['SourceCode']
    has_delegatecall = 'delegatecall' in source_code.lower()
    has_selfdestruct = 'selfdestruct' in source_code.lower() or 'suicide' in source_code.lower()

    holders_url = f"https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={contract_address}&page=1&offset=10&apikey={ETHERSCAN_API_KEY}"
    holders_resp = requests.get(holders_url).json()

    try:
        top_holders = holders_resp['result']
        total_top = sum([int(h['TokenHolderQuantity'].split('.')[0]) for h in top_holders])
        holders_count = len(top_holders)
        top_holder_ratio = max(int(top_holders[0]['TokenHolderQuantity'].split('.')[0]) / total_top, 0) if total_top > 0 else 0.0
    except:
        holders_count = 0
        top_holder_ratio = 1.0

    return {
        "is_verified": is_verified,
        "has_delegatecall": has_delegatecall,
        "has_selfdestruct": has_selfdestruct,
        "holders_count": holders_count,
        "top_holder_ratio": top_holder_ratio
    }
