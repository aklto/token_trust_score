from pycoingecko import CoinGeckoAPI
from datetime import datetime

cg = CoinGeckoAPI()

def get_token_data(token_id: str):
    data = cg.get_coin_by_id(token_id, localization=False)
    market_cap = data['market_data']['market_cap']['usd']
    volume = data['market_data']['total_volume']['usd']
    launch_date = data['genesis_date']
    age_days = (datetime.now() - datetime.strptime(launch_date, "%Y-%m-%d")).days if launch_date else 0
    return {'market_cap': market_cap, 'volume': volume, 'age_days': age_days}
