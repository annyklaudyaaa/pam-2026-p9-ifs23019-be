import json
import re

def parse_llm_response(result):
    try:
        content = result

        # Cari blok JSON di dalam teks (menggunakan regex agar lebih aman)
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if not match:
            raise Exception("Tidak ada JSON ditemukan dalam response")

        parsed = json.loads(match.group())

        # Cek key 'desserts' (untuk tema baru) atau fallback ke 'motivations' (untuk tema lama)
        # Jika keduanya tidak ada, return list kosong agar tidak crash
        return parsed.get("desserts") or parsed.get("motivations") or []

    except Exception as e:
        # Jika gagal parsing, kita lempar exception agar service bisa melakukan rollback
        raise Exception(f"Invalid JSON from LLM: {str(e)}")