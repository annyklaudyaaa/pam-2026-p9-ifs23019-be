from flask import Blueprint, request, jsonify
from app.services.dessert_service import (
    create_desserts,
    get_all_desserts
)

# Mengganti nama blueprint menjadi dessert
dessert_bp = Blueprint("dessert", __name__)

@dessert_bp.route("/", methods=["GET"])
def index():
    # Menyesuaikan dengan identitasmu
    return "API SweetAI telah berjalan! Dibuat oleh Anny Klaudya Hutabarat"

@dessert_bp.route("/desserts/generate", methods=["POST"])
def generate():
    data = request.get_json()
    theme = data.get("theme")
    total = data.get("total")

    if not theme:
        return jsonify({"error": "Bahan atau tema dessert wajib diisi"}), 400

    if not total:
        return jsonify({"error": "Jumlah total ide wajib diisi"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus lebih besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Maksimal pembuatan adalah 10 ide"}), 400

    try:
        # Memanggil service dessert_service yang baru
        result = create_desserts(theme, total)

        return jsonify({
            "theme": theme,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@dessert_bp.route("/desserts", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    # Default per_page disesuaikan menjadi 10 agar pas dengan UI Flutter
    per_page = request.args.get("per_page", default=10, type=int)

    data = get_all_desserts(page=page, per_page=per_page)

    return jsonify(data)