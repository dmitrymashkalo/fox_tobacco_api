from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_200_OK

from app.db.db import get_db
from app.models.brand import Brand, BrandCreate, BrandUpdate, Flavor

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/")
async def get_brands(db: AsyncSession = Depends(get_db)):
    """ Get all brands from db """
    brands = await db.execute(select(Brand))

    return {"brands": [brand for brand in brands.scalars()]}


@router.get("/with_flavors")
async def get_brands_with_flavor(db: AsyncSession = Depends(get_db)):
    """ Get all not empty brands """
    stmt = await db.execute(select(Brand).join(Flavor).distinct())
    brands = stmt.scalars().all()

    return brands


@router.post("/", status_code = status.HTTP_201_CREATED)
async def add_brand(brand: BrandCreate, db: AsyncSession = Depends(get_db)):
    """ Add new brand to db """
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


@router.put("/{brand_id}", status_code = status.HTTP_200_OK)
async def update_brand(brand_id: str, brand: BrandUpdate, db: AsyncSession = Depends(get_db)):
    """ Update existing brand """

    # get existing brand by id
    stmt = select(Brand).where(Brand.brand_id == brand_id)
    result = await db.execute(stmt)
    existing_brand = result.scalar_one_or_none()

    if not existing_brand:
        raise HTTPException(status_code=404, detail="Brand with this ID doesn't exist")

    # update info
    existing_brand.name = brand.name
    existing_brand.image_url = brand.image_url

    db.add(existing_brand)
    await db.commit()

    return {"message": "Brand updated"}


@router.delete("/{brand_id}", status_code=HTTP_200_OK)
async def delete_brand(brand_id: str, db: AsyncSession = Depends(get_db)):
    """ Delete existing brand """

    # get existing brand by id
    stmt = select(Brand).where(Brand.brand_id == brand_id)
    result = await db.execute(stmt)
    existing_brand = result.scalar_one_or_none()

    if not existing_brand:
        raise HTTPException(status_code=404, detail="Brand with this ID doesn't exist")

    await db.delete(existing_brand)
    await db.commit()

    return {"message": "Brand deleted"}