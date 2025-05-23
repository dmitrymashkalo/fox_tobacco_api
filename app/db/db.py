from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
import os
import ssl
import logging

# logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# check vars
if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    logger.error("Missing one or more PostgreSQL environment variables!")
    raise ValueError("Missing one or more PostgreSQL environment variables!")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERT_PATH = os.path.join(PROJECT_ROOT, "certs", "supabase_ca.crt")

logger.info(f"Attempting to use SSL certificate from: {CERT_PATH}")

# cerf exists check
if not os.path.exists(CERT_PATH):
    logger.error(f"SSL certificate file not found at: {CERT_PATH}")
    raise FileNotFoundError(f"SSL certificate file not found at: {CERT_PATH}")

ssl_context = ssl.create_default_context(
    cafile=CERT_PATH
)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = False

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "ssl": ssl_context,
        "timeout": 30,
    },
    pool_size=10,
    max_overflow=0,
    pool_recycle=55,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()