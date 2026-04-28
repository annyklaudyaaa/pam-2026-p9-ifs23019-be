from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Dessert(Base):
    __tablename__ = "desserts"

    id = Column(Integer, primary_key=True)
    # Kita gunakan 'name' agar sinkron dengan model di Flutter-mu
    name = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))