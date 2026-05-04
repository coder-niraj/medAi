from enum import Enum

from typing import Optional

from click import Option
from numpy import number
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class Result(str,Enum):
    green="green",
    yellow="yellow",
    red="red"
class Language(str,Enum):
    arabic="AR"
    english="EN"
class PatientActed(str,Enum):
    sought_care="sought_care" 
    monitored_at_home="monitored_at_home"
    ignored="ignored" 

class TriageResult(BaseModel):
  id: Optional[UUID] 
  session_id:Optional[UUID]  
  user_id:Optional[UUID]  = None
  result_level:Result
  urgency_score: Optional[int] 
  result_summary_enc:Optional[str] 
  result_recommendation_enc:Optional[str] 
  symptoms_reported_enc:Optional[str] 
  result_language:Language
  generated_at:datetime
  viewed_at:datetime = None
  patient_acted:PatientActed = None
