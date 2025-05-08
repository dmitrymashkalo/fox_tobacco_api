from app.db.db import Base
from sqlalchemy import Column, String


class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
