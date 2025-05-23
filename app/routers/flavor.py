from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.db import get_db
from app.models.brand import Flavor, Brand, FlavorCreate, FlavorUpdate

router = APIRouter(prefix="/flavors", tags=["Flavors"])


@router.get("/all")
async def get_flavor(db: AsyncSession = Depends(get_db)):
    """ Get all flavors from db """
    flavors = await db.execute(select(Flavor))

    return {"flavors": [flavor for flavor in flavors.scalars()]}


@router.get("/brand/{brand_id}")
async def get_flavors_with_qty(brand_id: str, db: AsyncSession = Depends(get_db)):
    """ Get all flavors by brand id where qty > 0 from db """
    flavors = await db.execute(select(Flavor).where(Flavor.available_qty > 0).join(Brand).where(Brand.brand_id==brand_id))

    return {"flavors": [flavor for flavor in flavors.scalars()]}


@router.get("/flavor/{flavor_id}")
async def get_flavor_details(flavor_id: str, db: AsyncSession = Depends(get_db)):
    """ Get flavor by flavor id """
    existing_flavor = await db.execute(select(Flavor).where(Flavor.flavor_id == flavor_id))

    if not existing_flavor:
        raise HTTPException(status_code=404, detail="Flavor with this ID doesn't exist")

    flavor = existing_flavor.scalars().first()

    return {"flavor": flavor}


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
        reserved_qty = flavor.reserved_qty if flavor.reserved_qty else None,
        image_url = str(flavor.image_url) if flavor.image_url else None,
        brand_id = brand_id
    )

    db.add(new_flavor)
    await db.commit()

    return {"message": "Flavor added"}


@router.put("/{flavor_id}", status_code = status.HTTP_200_OK)
async def update_flavor(flavor_id: str, flavor: FlavorUpdate, db: AsyncSession = Depends(get_db)):
    """ Update existing flavor """

    # get existing flavor by id
    stmt = select(Flavor).where(Flavor.flavor_id == flavor_id)
    result = await db.execute(stmt)
    existing_flavor = result.scalar_one_or_none()

    if not existing_flavor:
        raise HTTPException(status_code=404, detail="Flavor with this ID doesn't exist")

    update_data = flavor.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_flavor, field, value)

    db.add(existing_flavor)
    await db.commit()

    return {"message": "Flavor updated"}


@router.delete("/{flavor_id}", status_code=status.HTTP_200_OK)
async def delete_flavor(flavor_id: str, db: AsyncSession = Depends(get_db)):
    """ Delete existing flavor """

    # get existing flavor by id
    stmt = select(Flavor).where(Flavor.flavor_id == flavor_id)
    result = await db.execute(stmt)
    existing_flavor = result.scalar_one_or_none()

    if not existing_flavor:
        raise HTTPException(status_code=404, detail="Flavor with this ID doesn't exist")

    await db.delete(existing_flavor)
    await db.commit()

    return {"message": "Flavor deleted"}