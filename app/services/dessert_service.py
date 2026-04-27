from app.extensions import SessionLocal
from app.models.dessert import Dessert  # Pastikan import model Dessert yang baru
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_desserts(theme: str, total: int):
    session = SessionLocal()

    try:
        # Prompt disesuaikan untuk Dessert
        prompt = f"""
        Dalam format JSON, buat {total} rekomendasi dessert (makanan penutup) manis dengan keyword "{theme}".
        Setiap rekomendasi berisi nama dessert beserta deskripsi singkatnya dalam satu kalimat.
        Format:
        {{
            "desserts": [
                {{"name": "Nama Dessert: deskripsi singkat rasa dan tampilannya"}}
            ]
        }}
        Pastikan hanya kembalikan JSON saja, tanpa teks tambahan apapun.
        """

        result = generate_from_llm(prompt)
        # Ambil data dari parser (pastikan parser mencari key "desserts" atau "motivations")
        dessert_list = parse_llm_response(result)

        # Simpan log permintaan
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()

        saved = []

        for item in dessert_list:
            # Gunakan 'name' agar sinkron dengan model Dessert
            name_text = item.get("name") or item.get("text") # Fallback jika parser masih pakai 'text'

            d = Dessert(
                name=name_text,
                request_id=req_log.id
            )
            session.add(d)
            saved.append(name_text)

        session.commit()
        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_desserts(page: int = 1, per_page: int = 10):
    session = SessionLocal()

    try:
        query = session.query(Dessert)
        total = query.count()

        data = (
            query
            .order_by(Dessert.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        # Mapping data untuk dikirim ke Flutter
        result = [
            {
                "id": d.id,
                "name": d.name,
                "created_at": d.created_at.isoformat()
            }
            for d in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()