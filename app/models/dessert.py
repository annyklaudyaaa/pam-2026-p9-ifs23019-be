from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Dessert(Base):
    __tablename__ = "desserts"

    id = Column(Integer, primary_key=True)
    # Ganti 'text' jadi 'name' agar lebih cocok untuk nama makanan/kue
    name = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))