from app.extensions import SessionLocal
from app.models.dessert import Dessert  # Pastikan mengimpor model Dessert
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_desserts(theme: str, total: int):
    session = SessionLocal()
    try:
        # Prompt diubah agar LLM kasih Nama dan Deskripsi terpisah
        prompt = f"""
        Buatlah {total} ide dessert manis dengan tema "{theme}".
        Respon harus dalam format JSON:
        {{
            "desserts": [
                {{"name": "Nama Dessert", "description": "Deskripsi singkat satu kalimat"}}
            ]
        }}
        Hanya kembalikan JSON.
        """

        result = generate_from_llm(prompt)
        dessert_list = parse_llm_response(result)

        # Simpan log permintaan
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()
        session.refresh(req_log)

        saved = []
        for item in dessert_list:
            # Ambil name dan description secara terpisah
            name_text = item.get("name")
            desc_text = item.get("description", "") # Ambil deskripsi dari AI

            d = Dessert(
                name=name_text,
                description=desc_text, # Simpan ke kolom description
                request_id=req_log.id
            )
            session.add(d)
            saved.append({"name": name_text, "description": desc_text})

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

        # Mapping lengkap dengan description agar Flutter tidak error
        result = [
            {
                "id": d.id,
                "name": d.name,
                "description": d.description, # Kirim deskripsi ke Flutter
                "created_at": d.created_at.isoformat()
            }
            for d in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if total > 0 else 0,
            "data": result
        }
    finally:
        session.close()