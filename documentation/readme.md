Terms of Service TOS
Consent
Gender Range

APIS
Authentication
POST /auth/register
POST /auth/login
POST /auth/consent
POST /auth/guest-consent

Reports
POST /reports/upload — Updated
GET /reports
GET /reports/{report_id}/summary
GET /reports/{report_id}/file
DELETE /reports/{report_id}

Chat
POST /chat/sessions
GET /chat/sessions
POST /chat/sessions/{session_id}/messages
GET /chat/sessions/{session_id}/messages

Triage
POST /triage/complete/{session_id}
POST /triage/claim
GET /triage/results/{triage_result_id}
GET /triage/results
PATCH /chat/sessions/{session_id}/messages/{message_id}/feedback

User Data (PDPL Compliance)
GET /users/me/data-export
DELETE /users/me

Internal Fine-Tuning Endpoints (Admin Only)
POST /internal/ft-pipeline/run
GET /internal/ft-pipeline/stats

Health Status + LLM Traces Endpoints
GET /health
GET /internal/traces/{message_id}

The MENA region stands for:
Middle East and North Africa

AES-256 encrypted
HIPAA-listed identifier

user

id uuid
name str
email_encryoted str
phone_encrypted str
dob_encrypted str
prefered_language str
role enum
firebase_uid str
created_at date
consent_given_at timstamp
research_consent boolean
triage_count integer

guest

id uuid
guest_token str
tos_accepted boolean
research_consent boolean
age_range str
tos_accepted_At timestamp
gender str
nationality str
claimed_user_id uuid
created_at timestamp
expires_at timestamp

1. Why do we need Triage Result endpoints?
   You are right that the Chat Sessions endpoints manage the back-and-forth conversation. However, Triage Results are distinct for several structural and clinical reasons:

Finality & Persistence: A chat session is an ongoing stream of messages. A TriageResult is a finalized, structured record generated only after a session is complete. It stores the high-level medical outcome (Green/Yellow/Red status and urgency score) that the app needs to display on a specialized "Result Screen"

Data Structure: GET /triage/results/{id} returns specific fields that aren't in a standard chat message, such as urgency_score, symptoms_reported_enc (a summarized list of symptoms), and result_recommendation_enc

Unauthenticated Access (Guest Mode): The first triage session can be done by a guest. The system needs a way to store that specific result so a user can "claim" it later if they decide to create an account.

Safety Tracking: The triage_result is used for follow-up. For example, 48 hours after a "Red" or "Yellow" result, the system uses this record to trigger a push notification asking if the patient sought care.

2. The Nightly Pipeline
   The nightly pipeline is a set of automated background jobs that handle data cleanup and AI improvements. It includes:

Fine-tuning Curation (2 AM UTC): The system scans messages that are "eligible" for training (e.g., high-quality interactions where the user gave a good rating). It strips out Personal Health Information (PHI) and moves the data to a FINE_TUNING_EXAMPLES table to improve the AI's future accuracy.

Guest Session Cleanup (Every 6 hours): Deletes guest sessions and chats that are older than 24 hours and were never claimed by a registered user

Document Retention (3 AM UTC): Deletes medical reports and their associated embeddings after 2 years to comply with data privacy regulations.

Trace Retention (4 AM UTC): Since LLM traces are high-volume, the pipeline deletes the detailed prompt/response text after 90 days but keeps the metadata (like token counts) for long-term cost analysis.

3. What are LLM Traces?A Trace is a detailed log of a single "thought" or interaction by the AI. Every time the app calls the Gemini API, a row is written to the LLM_TRACES table. It is the primary tool for debugging and safety.

The Full Prompt: Exactly what text was sent to the AI, including the hidden system instructions and any retrieved document chunks.

The Raw Response: What the AI said before the safety guardrails checked it.

Guardrail Outcomes: Whether a safety filter (like the "cardiac urgency" check) was triggered to change the AI's answer.

Performance Data: How many tokens were used (for cost tracking) and how many milliseconds the AI took to respond.

Retrieval Metadata: In document chats, it records exactly which pieces of the medical report the AI "looked at" (chunk IDs and cosine similarity scores) to generate the answer.
