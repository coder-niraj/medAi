import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# app/db/session.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "core", "security", ".env") # Removed extra "app"

print(f"DEBUG: Looking for .env at: {ENV_PATH}") 
print(f"DEBUG: Does file exist? {os.path.exists(ENV_PATH)}")

load_dotenv(dotenv_path=ENV_PATH)
DB_url = os.getenv("DATABASE_URL")

engine = create_engine(
        DB_url, # type: ignore
        pool_pre_ping=True
    )
sessionLocal = sessionmaker(
        autocommit= False,
        autoflush=False,
        bind=engine
    )
# Dependency
def get_DB():
   db = sessionLocal()
   print("database connected")
   try:
    yield db
   finally:
    db.close()