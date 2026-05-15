import asyncio
from http import client
from urllib import response
from uuid import uuid4
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch
from sqlalchemy import inspect
from main import fast_app

FIREBASE_API = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
FIREBASE_API_KEY = "AIzaSyDujNAft2fmVCk6saJpYf12jt5fIFx1Q5o"
BASE_URL = "http://test"

USER_DATA_1 = {
    "name": "test1",
    "email": "test1@gmail.com",
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
async def firebase_token():
    async with AsyncClient() as client:
        response = await client.post(
            url=FIREBASE_API,
            params={"key": FIREBASE_API_KEY},
            json={
                "email": USER_DATA_1.get("email"),
                "password": USER_DATA_1.get("password"),
                "returnSecureToken": True,
            },
        )
        data = response.json()
        assert "idToken" in data, f"Firebase auth failed: {data}"
        return data["idToken"]


# * POST /auth/register
@pytest.fixture(scope="session")
async def user_register_success(firebase_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "firebase_id_token": firebase_token,
                "name": USER_DATA_1.get("name"),
                "dob": USER_DATA_1.get("dob"),
            },
        )

        return response.status_code


# * POST /auth/register
@pytest.fixture(scope="session")
async def user_register_success(firebase_token_gateway: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "firebase_id_token": firebase_token_gateway,
                "name": USER_DATA_1.get("name"),
                "dob": USER_DATA_1.get("dob"),
            },
        )

        return response.status_code


# * POST /auth/register
@pytest.fixture(scope="session")
async def user_re_register(firebase_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "firebase_id_token": firebase_token,
                "name": USER_DATA_1.get("name"),
                "dob": USER_DATA_1.get("dob"),
            },
        )
        print("_________", response.json())
        print("_________", response.status_code)
        return response.status_code


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_JWT(firebase_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login", json={"firebase_id_token": firebase_token}
        )
        assert response.status_code == 200
        return response.json()["access_token"]


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_response(firebase_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login", json={"firebase_id_token": firebase_token}
        )
        assert response.status_code == 200
        return response.json()


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_consent(firebase_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login", json={"firebase_id_token": firebase_token}
        )
        assert response.status_code == 200
        return response.json()["consent_given_at"]


# * POST /auth/consent
@pytest.fixture(scope="session")
async def JWT_consent_token(login_authentication_JWT: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/consent",
            headers={"Authorization": f"bearer {login_authentication_JWT}"},
            json={
                "tos_accepted": True,
                "research_consent": True,
                "phone_enc": USER_DATA_1.get("phone_env"),
            },
        )
        assert response.status_code in [200, 409], f"422 body: {response.json()}"

        data = response.json()

        if "access_token" in data:
            yield data["access_token"]
        else:
            yield login_authentication_JWT


# * POST /auth/consent
@pytest.fixture(scope="session")
async def invalid_JWT_consent_token():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/consent",
            headers={"Authorization": f"bearer fake_token"},
            json={
                "tos_accepted": True,
                "research_consent": True,
                "phone_enc": USER_DATA_1.get("phone_env"),
            },
        )
        return response.status_code


# * POST /auth/consent
@pytest.fixture(scope="session")
async def invalid_body_consent_token(login_authentication_JWT: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/consent",
            headers={"Authorization": f"bearer {login_authentication_JWT}"},
            json={
                "tos_accepted": False,
                "research_consent": False,
                "phone_enc": USER_DATA_1.get("phone_env"),
            },
        )

        return response.status_code


# * POST /auth/consent
@pytest.fixture(scope="session")
async def no_body_consent_token(login_authentication_JWT: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/consent",
            headers={"Authorization": f"bearer {login_authentication_JWT}"},
        )
        return response.status_code


# * POST /auth/register
@pytest.fixture(scope="session")
async def test_registration_invalid_token():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "firebase_id_token": "fake ",
                "name": USER_DATA_1.get("name"),
                "dob": USER_DATA_1.get("dob"),
            },
        )
        return response.status_code


# * POST /auth/register
@pytest.fixture(scope="session")
async def test_registration_no_body(JWT_consent_token: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={"firebase_id_token": JWT_consent_token},
        )
        return response.status_code


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_no_JWT():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post("/auth/login")
        return response.status_code


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_Invalid_JWT():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login", json={"firebase_id_token": "my token"}
        )
        return response.status_code


# * POST /auth/guest-consent
@pytest.fixture(scope="session")
async def guest_session_creation():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/guest-consent",
            headers={"X-Device-ID": str(uuid4())},
            json={
                "tos_accepted": True,
                "research_consent": True,
                "age_range": "1-10",
                "gender": "Male",
                "nationality": "American",
            },
        )
        print("______________", response.json())
        return response.status_code


# * POST /auth/guest-consent
@pytest.fixture(scope="session")
async def guest_session_validation():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/guest-consent",
            headers={"X-Device-ID": str(uuid4())},
            json={
                "tos_accepted": True,
            },
        )
        return response.status_code


# * POST /auth/guest-consent
@pytest.fixture(scope="session")
async def guest_session_response_validation():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/guest-consent",
            headers={"X-Device-ID": str(uuid4())},
            json={
                "tos_accepted": True,
                "research_consent": True,
                "age_range": "1-10",
                "gender": "Male",
                "nationality": "American",
            },
        )

        assert response.status_code in [200, 201, 400]
        return response.json()


@pytest.mark.asyncio
async def test_firebase_token_fetched(firebase_token):
    assert isinstance(firebase_token, str)
    assert len(firebase_token) > 10


@pytest.mark.asyncio
async def test_user_register(user_register_success):
    assert user_register_success in [200, 201, 409]


@pytest.mark.asyncio
async def test_user_re_register(user_re_register):
    assert user_re_register in [201, 200, 409]


@pytest.mark.asyncio
async def test_login_returns_jwt(login_authentication_JWT):
    assert isinstance(login_authentication_JWT, str)
    assert len(login_authentication_JWT) > 10


@pytest.mark.asyncio
async def test_invalid_JWT_consent_token(invalid_JWT_consent_token):
    assert invalid_JWT_consent_token in [409, 422, 500, 401]


@pytest.mark.asyncio
async def test_invalid_body_consent_token(invalid_body_consent_token):
    """Consent flow with a invalid body"""
    assert invalid_body_consent_token in [403, 422, 500, 401]


@pytest.mark.asyncio
async def test_no_body_consent_token(no_body_consent_token):
    assert no_body_consent_token in [409, 422, 500, 401]


@pytest.mark.asyncio
async def test_login_authentication_response(login_authentication_response):
    keys_to_check = [
        "access_token",
        "user_id",
        "preferred_language",
        "consent_given_at",
        "triage_count",
    ]
    result = all(k in login_authentication_response for k in keys_to_check)
    assert result == True


@pytest.mark.asyncio
async def test_login_authentication_consent(login_authentication_consent):
    assert login_authentication_consent is None or isinstance(
        login_authentication_consent, str
    )


@pytest.mark.asyncio
async def test_consent_token_exists(JWT_consent_token):
    assert isinstance(JWT_consent_token, str)
    assert len(JWT_consent_token) > 10


@pytest.mark.asyncio
async def test_full_auth_flow(JWT_consent_token, login_authentication_JWT):
    assert isinstance(JWT_consent_token, str)
    assert JWT_consent_token == login_authentication_JWT or len(JWT_consent_token) > 10


@pytest.mark.asyncio
async def test_user_register_no_body(test_registration_no_body):
    assert test_registration_no_body in [401, 422]


@pytest.mark.asyncio
async def test_user_register_invalid_token(test_registration_invalid_token):
    assert test_registration_invalid_token in [422, 401]


@pytest.mark.asyncio
async def test_login_no_token(login_authentication_no_JWT):
    assert login_authentication_no_JWT in [409, 422]


@pytest.mark.asyncio
async def test_login_invalid_token(login_authentication_Invalid_JWT):
    assert login_authentication_Invalid_JWT in [401, 500]


@pytest.mark.asyncio
async def test_guest_session_creation(guest_session_creation):
    assert guest_session_creation in [200, 201]


@pytest.mark.asyncio
async def test_guest_session_validation(guest_session_validation):
    assert guest_session_validation in [401, 422, 500]


@pytest.mark.asyncio
async def test_guest_session_response_validation(guest_session_response_validation):
    keys_to_check = ["guest_token", "expires_at"]
    result = all(k in guest_session_response_validation for k in keys_to_check)
    assert result == True


# def test_firebase_token_validation():
#     authenticated_user_api_calls("fn test")


# def jwt_generation_time_logic():
#     print("fn test")
