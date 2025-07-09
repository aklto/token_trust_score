
from openai import OpenAI
client = OpenAI()

def analyze_trust_score_with_llm(profile: dict) -> float:
    profile_str = "\n".join(f"{k}: {v}" for k, v in profile.items())
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты аналитик, оценивающий надёжность криптотокена."},
            {"role": "user", "content": f"Вот профиль токена:\n{profile_str}\nОцени trust score от 0.0 до 1.0 и верни только ЧИСЛО без текста."}
        ]
    )
    try:
        score_text = response.choices[0].message.content.strip()
        return max(0.0, min(1.0, float(score_text)))
    except Exception:
        return 0.5
    