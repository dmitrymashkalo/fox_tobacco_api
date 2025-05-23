import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("user")
DB_PASS = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")
