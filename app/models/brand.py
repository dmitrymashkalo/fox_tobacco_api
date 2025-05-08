from app.db.db import Base
from sqlalchemy import Column, String
from pydantic import BaseModel, HttpUrl
from typing import Union


class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)


class BrandCreate(BaseModel):
    brand_id: str
    name: str
    image_url: Union[HttpUrl, None] = None


class BrandUpdate(BaseModel):
    name: str
    image_url: Union[HttpUrl, None] = None


class BrandDelete(BaseModel):
    brand_id: str
