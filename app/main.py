from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.db.db import engine, Base
from app.routers import brand, flavor
import uvicorn

app = FastAPI()

# routers
app.include_router(brand.router)
app.include_router(flavor.router)


#@app.on_event("startup")
#async def startup():
    # Create all tables
    # async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)