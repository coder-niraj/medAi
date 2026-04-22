import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from utils.events import init_pubsub
from db.session import engine
from db.base import Base
from helpers.index import (
    logger,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from routes.index import router

# from models.auditLogs import AuditHook
# from models.chatMessage import ChatMessage
# from models.chatSessions import ChatSession
# from models.clinicalReview import ClinicianReview

# # from models.embeddings import ReportEmbedding
# from models.extension import ExtensionHook
# from models.fineTuning import FineTuningExample
# from models.guest import GuestSession
# from models.triage import TriageResult
# from models.reports import Report
# from models.lab import LabValue
# from models.llm import LLMTrace
# from models.patient import PatientDemographics
# from models.user import User

# ✅ Load ENV correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "app", "core", "security", ".env")
load_dotenv(dotenv_path=ENV_PATH)

fast_app = FastAPI()
init_pubsub()

# ✅ Middleware
fast_app.middleware("http")(logger)

# ✅ CORS
fast_app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=["*"],
)
Base.metadata.create_all(bind=engine)

# all Error Handlers attechment
fast_app.add_exception_handler(
    RequestValidationError, validation_exception_handler  # type: ignore[arg-type]
)
fast_app.add_exception_handler(
    HTTPException, http_exception_handler  # type: ignore[arg-type]
)
fast_app.add_exception_handler(Exception, global_exception_handler)
fast_app.include_router(router)

print("Server will run on port:", os.getenv("PORT", "8000"))
