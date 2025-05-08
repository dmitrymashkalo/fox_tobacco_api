from app.db.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, HttpUrl
from typing import Union


class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    flavors = relationship("Flavor", back_populates="brand", cascade="all, delete-orphan")


class Flavor(Base):
    __tablename__ = "flavors"

    flavor_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    available_qty = Column(Integer, nullable=False)
    photo_url = Column(String, nullable=True)

    brand_id = Column(String, ForeignKey("brands.brand_id"), nullable=False)
    brand = relationship("Brand", back_populates="flavors")


class BrandCreate(BaseModel):
    brand_id: str
    name: str
    image_url: Union[HttpUrl, None] = None


class BrandUpdate(BaseModel):
    name: str
    image_url: Union[HttpUrl, None] = None


class FlavorCreate(BaseModel):
    flavor_id: str
    name: str
    weight: str
    price: int
    description: str
    available_qty: int
    photo_url: Union[HttpUrl, None] = None
