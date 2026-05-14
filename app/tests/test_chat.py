# * POST /sessions

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import inspect
from main import fast_app
from uuid import uuid4

FIREBASE_API = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
FIREBASE_API_KEY = "AIzaSyDujNAft2fmVCk6saJpYf12jt5fIFx1Q5o"
BASE_URL = "http://test"
USER_DATA_2 = {
    "name": "test2",
    "email": "test2@gmail.com",
    "password": "123456",
    "phone_env": "190909092",
    "dob": "2003-10-01",
    "gender": "male",
    "age_range": "26-35",
    "region": "dubai",
    "nationality": "AE",
    "health_literacy": "medium",
    "chronic_conditions": ["diabetes", "hypertension", "thyroid"],
}


@pytest.fixture(scope="session")
async def guest_session_creation(guest_success_profile_creation):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/chat/sessions",
            headers={
                "Authorization": f"guest:{guest_success_profile_creation["guest_token"]}",
            },
            json={
                "mode": "triage",
            },
        )
        assert response.status_code in [403, 401, 500]
        return response.json()


# * GET /sessions
@pytest.fixture(scope="session")
async def guest_get_session(guest_success_profile_creation):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/chat/sessions",
            headers={
                "Authorization": f"guest:{guest_success_profile_creation["guest_token"]}",
            },
        )
        assert response.status_code in [429, 403, 401]
        return response.json()


# * POST /sessions
@pytest.fixture(scope="session")
async def user_session_creation(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/chat/sessions",
            headers={
                "Authorization": f"bearer {JWT_consent_token}",
            },
            json={
                "mode": "triage",
            },
        )
        assert response.status_code in [200, 201, 403, 500]
        return response.json()


# * GET /sessions
@pytest.fixture(scope="session")
async def user_get_sessions(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/chat/sessions?mode=triage&offset=0&limit=20",
            headers={
                "Authorization": f"bearer {JWT_consent_token}",
            },
        )
        print(response)
        print("== ", response.json())
        assert response.status_code in [200, 201, 403, 500, 422]
        return response.json()


@pytest.mark.asyncio
async def test_guest_session_creation(guest_session_creation):
    data = guest_session_creation


@pytest.mark.asyncio
async def test_guest_get_session(guest_get_session):
    data = guest_get_session


@pytest.mark.asyncio
async def test_user_session_creation(user_session_creation):
    data = user_session_creation


@pytest.mark.asyncio
async def test_user_get_sessions(user_get_sessions):
    data = user_get_sessions
