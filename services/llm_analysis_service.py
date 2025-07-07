import re
import openai
import os
from functools import lru_cache

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@lru_cache(maxsize=500)
def analyze_trust_score_with_llm(profile: str) -> float:
    print("🧾 Token Profile (for LLM):\n", profile)

    prompt = f"""
Ты эксперт по безопасности криптовалют. Оцени риск токена по следующему профилю:

{profile}

Ответь строго одним числом от 0.0 (максимальный риск) до 1.0 (надежный токен).
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    text = response.choices[0].message.content
    match = re.search(r"\d\.\d+", text)
    return float(match.group()) if match else 0.0
