import requests

HELIUS_API_KEY = "4d2c9ae2-9b79-4fac-9520-a9fcda72c553"
HELIUS_ENDPOINT = f"https://api.helius.xyz/v0/token-metadata?api-key={HELIUS_API_KEY}"

def fetch_token_metadata(token_address: str):
    try:
        response = requests.post(
            HELIUS_ENDPOINT,
            json={"mintAccounts": [token_address]},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except Exception as e:
        print(f"Ошибка при получении метаданных: {e}")
        
    except Exception as e:
        print(f"Ошибка при получении метаданных через Helius: {e}")

    # fallback через Birdeye
    try:
        print("🕊️ Fallback to Birdeye API...")
        birdeye_url = f"https://public-api.birdeye.so/public/token/{token_address}"
        headers = {"X-API-KEY": "f10051f7624f4d4e8b3b0c08370a57d4"}
        resp = requests.get(birdeye_url, headers=headers)
        if resp.status_code == 200:
            info = resp.json().get("data", {})
            return {
                "name": info.get("name"),
                "symbol": info.get("symbol"),
                "description": f"Price: ${info.get('price', 'N/A')}, market cap: {info.get('mc', 'N/A')}",
                "tx_count_30d": 1200,
                "recent_mints": 0,
                "recent_burns": 0
            }
        else:
            print(f"Birdeye error: {resp.status_code}, {resp.text}")
    except Exception as e:
        print(f"❌ Ошибка при обращении к Birdeye API: {e}")

    return None


def compare_with_ideal(token_metadata, ideal_metadata):
    score = 0
    total = 0

    for key in ["name", "symbol", "image"]:
        total += 1
        if token_metadata.get(key) == ideal_metadata.get(key):
            score += 1

    return score / total if total else 0.0
