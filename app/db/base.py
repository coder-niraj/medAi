# db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.user import User
from models.patient import PatientDemographics
from models.reports import Report
from models.auditLogs import AuditHook
from models.chatMessage import ChatMessage
from models.chatSessions import ChatSession
from models.clinicalReview import ClinicianReview
from models.extension import ExtensionHook
from models.fineTuning import FineTuningExample
from models.guest import GuestSession
from models.triage import TriageResult
from models.lab import LabValue
from models.llm import LLMTrace