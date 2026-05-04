import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.extension import ExtensionHook

dummy_extension_hooks = [
    # 1. Ahmed — telemedicine enabled, active
    {
        "id": uuid.UUID("9f440c59-a3a0-4863-8901-b72b1dd63966"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "hook_name": "telemedicine_enabled",
        "hook_value": {
            "provider": "seha",
            "provider_display_name": "Seha Virtual Care",
            "redirect_url": "https://seha.ae/consult",
            "preferred_language": "ar",
            "preferred_slot": "morning",
            "auto_escalate_red_triage": True,
        },
        "is_active": True,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 2. Ahmed — whatsapp followup enabled, active
    #    triggers on yellow and red triage results
    {
        "id": uuid.UUID("c428536d-bf9f-47d3-8ad7-5254eac86ed7"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "hook_name": "whatsapp_followup_enabled",
        "hook_value": {
            "whatsapp_number": "+966500000000",
            "followup_delay_hours": 48,
            "trigger_on": ["yellow", "red"],
            "message_language": "ar",
            "opt_out_token": "abc123xyz",
        },
        "is_active": True,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 3. Sarah — payment gateway configured,
    #    is_active = False — post MVP feature not yet enabled
    {
        "id": uuid.UUID("4a16e77d-3142-4f7f-83eb-c3ac9043ba2c"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "hook_name": "payment_gateway_url",
        "hook_value": {
            "gateway": "moyasar",
            "gateway_display_name": "Moyasar",
            "publishable_key": "pk_test_placeholder",
            "currency": "SAR",
            "billable_features": ["triage_session", "document_upload"],
            "free_tier_limit": {
                "triage_sessions": 1,
                "document_uploads": 0,
            },
        },
        "is_active": False,             # not yet activated
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 4. Sarah — physician escalation webhook,
    #    triggers on red triage only, active
    {
        "id": uuid.UUID("af4c055c-9f0c-4d16-b46e-04e7e58350af"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "hook_name": "physician_escalation_webhook",
        "hook_value": {
            "webhook_url": "https://internal.clinic-system.sa/api/escalate",
            "auth_header": "X-Webhook-Secret",
            "secret_ref": "projects/med-ai/secrets/clinic_webhook_secret/versions/latest",
            "trigger_on": ["red"],
            "include_fields": [
                "session_id",
                "urgency_score",
                "symptoms_reported",
                "result_summary",
            ],
            "timeout_seconds": 10,
            "retry_attempts": 3,
        },
        "is_active": True,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },
]



def seed_extension_hooks(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_extension_hooks:
        db.merge(ExtensionHook(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_extension_hooks)} extension hooks")