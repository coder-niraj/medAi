from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.db.session import engine
from app.db.base import Base
from app.helpers.index import logger
from app.routes.index import router

# ✅ Load ENV correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "app", "core", "security", ".env")
load_dotenv(dotenv_path=ENV_PATH)

fast_app = FastAPI()

# ✅ CORS
fast_app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=["*"]
)

# ✅ Middleware
fast_app.middleware("http")(logger)
Base.metadata.create_all(bind=engine)
# fast_app.add_exception_handler(HTTPException, errorHandler)
# fast_app.add_exception_handler(RequestValidationError, validation_exception_handler)

# ✅ Routes
fast_app.include_router(router)

print("Server will run on port:", os.getenv("PORT", "8000"))