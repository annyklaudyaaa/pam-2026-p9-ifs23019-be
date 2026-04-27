import requests
from app.config import Config

def generate_from_llm(prompt: str):
    # Menggunakan OpenRouter API
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {Config.LLM_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            # Jika model Nemotron sedang sibuk atau limit tercapai,
            # kamu bisa mempertimbangkan 'google/gemini-pro-1.5-exp:free'
            # atau 'mistralai/mistral-7b-instruct:free' untuk respon yang lebih cepat.
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7 # Tambahkan ini agar ide dessert lebih kreatif
        }
    )

    if response.status_code != 200:
        raise Exception("LLM request failed: " + response.text)

    # Mengambil konten teks dari respon JSON
    return response.json()["choices"][0]["message"]["content"]