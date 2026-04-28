from app.extensions import SessionLocal
from app.models.dessert import Dessert  # Pastikan mengimpor model Dessert
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_desserts(theme: str, total: int):
    session = SessionLocal()

    try:
        # Prompt fokus ke hidangan penutup (Dessert)
        prompt = f"""
        Dalam format JSON, buat {total} rekomendasi dessert (makanan penutup) manis dengan keyword "{theme}".
        Setiap rekomendasi berisi nama dessert beserta deskripsi singkatnya dalam satu kalimat.
        Format:
        {{
            "desserts": [
                {{"name": "Nama Dessert: deskripsi singkat dessert tersebut"}}
            ]
        }}
        Pastikan hanya kembalikan JSON saja, tanpa teks tambahan apapun.
        """

        result = generate_from_llm(prompt)
        # Parser akan mencari key 'desserts' sesuai prompt di atas
        dessert_list = parse_llm_response(result)

        # Simpan log permintaan ke tabel requests
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()

        saved = []

        for item in dessert_list:
            # Mengambil 'name' sesuai dengan model Dessert yang kita buat sebelumnya
            name_text = item.get("name")

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
        # Mengambil data dari tabel desserts
        query = session.query(Dessert)
        total = query.count()

        data = (
            query
            .order_by(Dessert.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        # Mapping ke format JSON untuk Flutter (menggunakan key 'name')
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