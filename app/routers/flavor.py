from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.db import get_db
from app.models.brand import Flavor, Brand, FlavorCreate

router = APIRouter(prefix="/flavors", tags=["Flavors"])


@router.get("/")
async def get_flavor(db: AsyncSession = Depends(get_db)):
    """ Get all flavors from db """
    flavors = await db.execute(select(Flavor))
    return {"flavors": [flavor for flavor in flavors.scalars()]}


@router.post("/{brand_id}", status_code = status.HTTP_201_CREATED)
async def add_flavor(brand_id: str, flavor: FlavorCreate, db: AsyncSession = Depends(get_db)):
    """ Add new flavor to db """
    # verify existing flavors
    existing_flavor = await db.execute(select(Flavor).where(Flavor.flavor_id == flavor.flavor_id))
    existing_brand = await db.execute(select(Brand).where(Brand.brand_id == brand_id))

    # return 400 if flavor exists
    if existing_flavor.scalar():
        raise HTTPException(status_code=400, detail="Flavor with this ID exists")
    # return 404 if brand doesn't exist
    if not existing_brand:
        raise HTTPException(status_code=404, detail="Brand with this ID doesn't exist")

    # create new flavor
    new_flavor = Flavor(
        flavor_id = flavor.flavor_id,
        name = flavor.name,
        weight = flavor.weight,
        price = flavor.price,
        description = flavor.description,
        available_qty = flavor.available_qty,
        photo_url = flavor.photo_url,
        brand_id = brand_id
    )

    db.add(new_flavor)
    await db.commit()

    return {"message": "Flavor added"}