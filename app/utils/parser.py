import json
import re

def parse_llm_response(result):
    try:
        content = result

        # 1. Gunakan Regex untuk mengambil blok JSON (mengantisipasi teks tambahan dari LLM)
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if not match:
            raise Exception("Tidak ada JSON ditemukan dalam response")

        # 2. Decode string menjadi dictionary Python
        parsed = json.loads(match.group())

        # 3. Ambil data dengan urutan prioritas:
        # Cek 'desserts' dulu, jika tidak ada cek 'motivations', jika tidak ada beri list kosong
        data = parsed.get("desserts") or parsed.get("motivations") or []

        return data

    except Exception as e:
        # Melempar error agar bisa ditangkap oleh blok try-except di Service Layer
        raise Exception(f"Gagal memproses JSON dari AI: {str(e)}")