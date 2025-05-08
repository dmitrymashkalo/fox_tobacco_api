from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db

app = FastAPI()


@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 'Hello from DB'"))
    return {"message": result.scalar()}
