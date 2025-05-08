from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.db import get_db
from app.models.brand import Brand

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.get("/")
async def get_brands(db: AsyncSession = Depends(get_db)):
    """ Get all brands from db"""
    brands = await db.execute(select(Brand))
    return {"brands": [brand.name for brand in brands.scalars()]}