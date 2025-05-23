from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.db.db import engine, Base
from app.routers import brand, flavor
import uvicorn

app = FastAPI()

# routers
app.include_router(brand.router)
app.include_router(flavor.router)

@app.get("/")
async def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)