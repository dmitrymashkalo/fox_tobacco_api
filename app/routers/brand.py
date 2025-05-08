from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.db import get_db
from app.models.brand import Brand, BrandCreate

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.get("/")
async def get_brands(db: AsyncSession = Depends(get_db)):
    """ Get all brands from db"""
    brands = await db.execute(select(Brand))
    return {"brands": [brand for brand in brands.scalars()]}


@router.post("/", status_code = status.HTTP_201_CREATED)
async def add_brand(brand: BrandCreate, db: AsyncSession = Depends(get_db)):
    # verify existing brands
    existing = await db.execute(select(Brand).where(Brand.brand_id == brand.brand_id))

    # return 400 if brand exists
    if existing.scalar():
        raise HTTPException(status_code=400, detail="Brand with this ID exists")

    # create new brand
    new_brand = Brand(
        brand_id=brand.brand_id,
        name=brand.name,
        image_url=brand.image_url
    )
    db.add(new_brand)
    await db.commit()

    return {"message": "Brand added"}