from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.extensions import Base

class Dessert(Base):
    __tablename__ = "desserts"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False) # Nama boneka/tanaman
    
    # Tambahkan kolom deskripsi untuk menyimpan hasil dari LLM
    description = Column(Text, nullable=True) 
    
    # Tambahkan kolom image_url untuk menyimpan link gambar (misal dari placeholder atau AI)
    image_url = Column(String(255), nullable=True)
    
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Opsional: Agar lebih mudah dikonversi ke JSON di route
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat()
        }