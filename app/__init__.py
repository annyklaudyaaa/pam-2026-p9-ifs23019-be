from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
# Menambahkan 's' agar sesuai dengan dessert_routes.py
from app.routes.dessert_routes import dessert_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS agar aplikasi Flutter kamu bisa "ngobrol" dengan Backend ini
    CORS(app)

    # Secara otomatis membuat tabel 'desserts' dan 'requests' di database
    # Ini penting agar kamu tidak perlu buat tabel manual di MySQL/SQLite
    Base.metadata.create_all(bind=engine)

    # Registrasi blueprint agar rute /desserts bisa diakses
    app.register_blueprint(dessert_bp)

    return app