from fastapi import FastAPI
from app.db.db import engine, Base
from app.routers import brand
import uvicorn

app = FastAPI()

# routers
app.include_router(brand.router)

@app.on_event("startup")
async def startup():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)