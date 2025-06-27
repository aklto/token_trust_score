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
        return None

def compare_with_ideal(token_metadata, ideal_metadata):
    score = 0
    total = 0

    for key in ["name", "symbol", "image"]:
        total += 1
        if token_metadata.get(key) == ideal_metadata.get(key):
            score += 1

    return score / total if total else 0.0
