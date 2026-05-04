from db.session import sessionLocal
from services.seeding.chatMessage import seed_chat_messages
from services.seeding.chatSession import seed_chat_sessions
from services.seeding.clinical import seed_clinician_reviews
from services.seeding.demographics import seed_patient_demographics
from services.seeding.extension import seed_extension_hooks
from services.seeding.fineTuning import seed_fine_tuning_examples
from services.seeding.guest import seed_guest_sessions
from services.seeding.labValues import seed_lab_values
from services.seeding.llmTraces import seed_llm_traces
from services.seeding.report import seed_reports
from services.seeding.triage import seed_triage_results
from services.seeding.user import seed_users


def run_all_seeds():
    db = sessionLocal()
    try:
        seed_users(db)                    # 1. no FK dependencies
        seed_guest_sessions(db)           # 2. FK → users
        seed_reports(db)                  # 3. FK → users
        seed_patient_demographics(db)     # 4. FK → users
        seed_chat_sessions(db)            # 5. FK → users, reports
        seed_chat_messages(db)            # 6. FK → chat_sessions
        seed_triage_results(db)           # 7. FK → chat_sessions, users
        seed_llm_traces(db)               # 8. FK → chat_sessions, messages, reports
        seed_lab_values(db)               # 9. FK → reports
        seed_fine_tuning_examples(db)     # 10. no hard FK
        seed_extension_hooks(db)          # 11. FK → users
        seed_clinician_reviews(db)
    except Exception as e:
          print("error occurred ",e)