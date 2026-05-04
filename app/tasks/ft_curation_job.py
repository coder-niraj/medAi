from ast import Return
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.db.session import sessionLocal
from app.models import user
from app.models.chatMessage import ChatMessage
from app.models.chatSessions import ChatSession
from app.models.user import User
from app.models.patient import PatientDemographics

from app.models.fineTuning import FineTuningExample


def run():
    print("nightly fine tuning pipeline ________")
    db = sessionLocal()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    result = db.execute(
        select(ChatMessage).filter(
            ChatMessage.role == "assistant",
            ChatMessage.created_at > cutoff,
            ChatMessage.ft_eligible.is_(None),
        )
    )
    messages = result.scalars().all()
    eligible_count = 0
    phi_fail_count = 0
    for message in messages:
        is_eligible = is_eligible(db, message.ft_eligible)
        if not is_eligible:
            mark_message(db, message, eligible=False, reason="failed_eligibility_rules")
            continue
        if not check_user_research_consent(db, message.session_id):
            mark_message(db, message, eligible=False, reason="no_research_consent")
            continue
        stripped_question = strip_phi(message)
        stripped_response = strip_phi(message)
        stripped_context = strip_phi(message or "")
        phi_found = (
            scan_for_phi(stripped_question)
            or scan_for_phi(stripped_response)
            or scan_for_phi(stripped_context)
        )
        if phi_found:
            phi_fail_count += 1
            mark_message(db, message, eligible=False, reason="phi_scan_failed")
            continue
        user_obj = get_user_from_session(db, message.session_id)
        demographic_data = db.execute(
            select(PatientDemographics).filter(
                PatientDemographics.user_id == user_obj.id
            )
        ).scalar_one_or_none()


def is_eligible(db: Session, message: ChatMessage):
    if message.guardrail_triggered:
        return False
    if message.fallback_used:
        return False
    message_session = (
        db.query(ChatSession).filter(ChatSession.id == message.session_id).first()
    )
    if not message_session:
        return False
    if message_session.is_guest:
        return False
    if message_session.triage_status == "abandoned":
        return False
    if message.patient_rating is not None and message.patient_rating < 4:
        return False

    return True


def mark_message(db: Session, message: ChatMessage, eligible: bool, reason: str = None):

    db.query(ChatMessage).filter(ChatMessage.id == message.id).update(
        {"ft_eligible": eligible, "ft_excluded_reason": reason}
    )
    db.commit()


def check_user_research_consent(db: Session, message_session_id):
    message_session = (
        db.query(ChatSession).filter(ChatSession.id == message_session_id).first()
    )
    user_obj = db.query(User).filter(User.id == message_session.user_id).first()
    if not user_obj or not user_obj.research_consent:
        return False


def get_user_from_session(db: Session, message_session_id):
    message_session = (
        db.query(ChatSession).filter(ChatSession.id == message_session_id).first()
    )
    user_obj = db.query(User).filter(User.id == message_session.user_id).first()
    return user_obj


def strip_phi(mag):
    return True


def scan_for_phi(mag):
    return True
