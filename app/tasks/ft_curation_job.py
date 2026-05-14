import json
from sqlalchemy import select
from models import user
from models.chatMessage import ChatMessage
from models.chatSession import ChatSession
from services.seeding import report
from repository.finetune.index import FineTuneRepo
from repository.chat.index import ChatRepo
from db.session import sessionLocal
from models.patient import PatientDemographics
from services.encryption_service import AES256Service


def run():
    enc_obj = AES256Service()
    db = sessionLocal()
    chat_repo = ChatRepo(db=db)
    ft_repo = FineTuneRepo(db=db)

    print("nightly fine tuning pipeline ________")
    messages = chat_repo.get_non_finetuned_assistant_response_messages()
    if not messages:
        print("No messages to process")
        db.close()
        return
    eligible_count = 0
    phi_fail_count = 0
    to_insert = []
    session_ids = list(set(message.session_id for message in messages))
    session_objs = chat_repo.get_session_ids_from_messages(messages)
    user_objs = chat_repo.get_users_from_sessions(session_objs)
    report_objs = chat_repo.get_reports_from_sessions(session_objs)
    all_message_history_objs = chat_repo.get_all_messages_group_by_session(session_ids)
    user_ids = list(user_objs.keys())
    demographic_objs = chat_repo.get_demographics_data(user_ids)

    for message in messages:
        session_id = message.session_id
        session_obj = session_objs.get(str(session_id))
        user_obj = user_objs.get(str(session_obj.user_id))
        demographic_obj = demographic_objs.get(str(session_obj.user_id))
        all_session_msgs = all_message_history_objs.get(str(session_id), [])
        report_obj = (
            report_objs.get(str(session_obj.report_id))
            if session_obj.report_id
            else None
        )

        # * eligible for fine tune (if already fine tuned then false)

        if not is_eligible(message, session_obj):
            chat_repo.mark_message(
                message, eligible=False, reason="failed_eligibility_rules"
            )
            continue

        # * research consent is accepted
        if not user_obj or not user_obj.research_consent:
            print("________research consent")
            chat_repo.mark_message(
                message, eligible=False, reason="no_research_consent"
            )
            continue

        # * get all message response and question
        prior_msgs = [m for m in all_session_msgs if m.created_at < message.created_at]
        conversation_history = []
        for msg in prior_msgs:
            content_plain = enc_obj.decrypt(msg.content_enc)
            stripped = strip_phi(content_plain)
            conversation_history.append(
                {
                    "role": msg.role,
                    "content": stripped,
                }
            )

        # * get assistant message user message
        assistant_msg = message.content_enc
        user_msg = next((m for m in reversed(prior_msgs) if m.role == "user"), None)

        # * decrypt message and response
        assistant_text = enc_obj.decrypt(assistant_msg) if assistant_msg else ""
        user_text = enc_obj.decrypt(user_msg.content_enc) if user_msg else ""

        # TODO: CTO START
        # * PHI stripping and converting
        stripped_question = strip_phi(user_text)
        stripped_response = strip_phi(assistant_text)
        stripped_context = strip_phi(json.dumps(conversation_history))
        phi_found = (
            scan_for_phi(stripped_question)
            or scan_for_phi(stripped_response)
            or scan_for_phi(stripped_context)
        )

        # * PHI scanning
        if phi_found:
            phi_fail_count += 1
            chat_repo.mark_message(message, eligible=False, reason="phi_scan_failed")
            continue
        # ! CTO END

        # * get system prompt from environment
        system_prompt = get_system_prompt_for_session(
            mode=session_obj.mode,
            report_type=(
                report_obj.report_type if report_obj else None
            ),  # None for triage/general
        )
        triage_result_level = None
        document_quality = report_obj.document_quality if report_obj else Non

        # * finetune object creation
        to_insert.append(
            ft_repo.build_object(
                message=message,
                report_obj=report_obj,
                session_obj=session_obj,
                system_prompt=system_prompt,
                stripped_context=stripped_context,
                conversation_history=conversation_history,
                stripped_question=stripped_question,
                stripped_response=stripped_response,
                triage_result_level=triage_result_level,
                document_quality=document_quality,
                demographic_obj=demographic_obj,
            )
        )
        chat_repo.mark_message(message, eligible=True)
        eligible_count += 1
    if to_insert:
        ft_repo.bulk_insert(to_insert)


def strip_phi(text):
    return text  # no-op for now


def scan_for_phi(text):
    return False  # assume safe


def get_system_prompt_for_session(mode, report_type):
    return ""


def is_eligible(message: ChatMessage, session_obj: ChatSession):
    if message.guardrail_triggered:
        return False
    if message.fallback_used:
        return False

    if not session_obj:
        return False
    if session_obj.is_guest:
        return False
    if session_obj.triage_status == "abandoned":
        return False
    if message.patient_rating is not None and message.patient_rating < 4:
        return False

    return True
