import requests
from app.config import Config

def generate_from_llm(prompt: str):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {Config.LLM_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code != 200:
        raise Exception("LLM request failed: " + response.text)

    return response.json()["choices"][0]["message"]["content"]