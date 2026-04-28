from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.dessert_routes import dessert_bp

def create_app():
    app = Flask(__name__)

    # Perbaikan di sini: Tambahkan pengaturan origin agar Flutter Web tidak diblokir
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Secara otomatis membuat tabel 'desserts' dan 'requests' di database
    Base.metadata.create_all(bind=engine)

    # Registrasi blueprint
    app.register_blueprint(dessert_bp)

    return app