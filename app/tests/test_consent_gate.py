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

# {
#     "user_id": "9cf55725-9576-41cf-9cf3-8a51701d22bd",
#     "name": "niraj",
#     "preferred_language": "en",
#     "email_enc": "nirajparekh.work@gmail.com",
#     "dob_enc": "2003-10-01"
# }


@pytest.fixture(scope="session")
async def firebase_token_gateway():
    async with AsyncClient() as client:
        response = await client.post(
            url=FIREBASE_API,
            params={"key": FIREBASE_API_KEY},
            json={
                "email": USER_DATA_2.get("email"),
                "password": USER_DATA_2.get("password"),
                "returnSecureToken": True,
            },
        )
        data = response.json()
        print("______", data)
        assert "idToken" in data, f"Firebase auth failed: {data}"
        return data["idToken"]


# * POST /auth/register
@pytest.fixture(scope="session")
async def user_register_success_gateway(firebase_token_gateway: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/register",
            json={
                "firebase_id_token": firebase_token_gateway,
                "name": USER_DATA_2.get("name"),
                "dob": USER_DATA_2.get("dob"),
            },
        )

        return response.status_code


# * POST /auth/login
@pytest.fixture(scope="session")
async def login_authentication_gateway(firebase_token_gateway: str):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login", json={"firebase_id_token": firebase_token_gateway}
        )
        print("here ", response.status_code)
        print("here ", response.json())
        assert response.status_code == 200
        return response.json()


# * POST /auth/guest-consent
@pytest.fixture(scope="session")
async def guest_profile_creation():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/guest-consent",
            headers={"X-Device-ID": str(uuid4())},
            json={
                "tos_accepted": False,
                "research_consent": False,
                "age_range": "1-10",
                "gender": "Male",
                "nationality": "American",
            },
        )
        assert response.status_code in [200, 201, 429]
        return response.json()


# * POST /auth/guest-consent
@pytest.fixture(scope="session")
async def guest_success_profile_creation():
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
        assert response.status_code in [200, 201, 429]
        return response.json()


# * POST /sessions
@pytest.fixture(scope="session")
async def guest_session_creation(guest_profile_creation):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/chat/sessions",
            headers={
                "Authorization": f"guest:{guest_profile_creation["guest_token"]}",
            },
            json={
                "mode": "triage",
            },
        )
        assert response.status_code in [403, 401, 500]
        return response.json()


# * GET /sessions
@pytest.fixture(scope="session")
async def guest_get_session(guest_profile_creation):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/chat/sessions",
            headers={
                "Authorization": f"guest:{guest_profile_creation["guest_token"]}",
            },
            # json={"mode": "triage", "limit": 20, "offset": 0},
        )
        assert response.status_code in [429, 403, 401]
        return response.json()


# * GET /sessions
@pytest.fixture(scope="session")
async def user_get_sessions(login_authentication_gateway):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/chat/sessions",
            headers={
                "Authorization": f"bearer {login_authentication_gateway["access_token"]}",
            },
            # json={"mode": "triage", "limit": 20, "offset": 0},
        )
        assert response.status_code in [401, 429, 403]
        return response.json()


# * POST /sessions
@pytest.fixture(scope="session")
async def user_session_creation(login_authentication_gateway):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/chat/sessions",
            headers={
                "Authorization": f"bearer {login_authentication_gateway["access_token"]}",
            },
            json={
                "mode": "triage",
            },
        )
        assert response.status_code in [403, 401, 429]
        return response.json()


@pytest.mark.asyncio
async def test_user_register_success_gateway(user_register_success_gateway):
    assert user_register_success_gateway in [200, 409, 500, 201]


@pytest.mark.asyncio
async def test_login_authentication_consent(login_authentication_gateway):
    consent = login_authentication_gateway["consent_given_at"]
    access_token = login_authentication_gateway["access_token"]
    print("helo ", login_authentication_gateway)
    assert consent is None


@pytest.mark.asyncio
async def test_guest_session_creation(guest_session_creation):
    data = guest_session_creation
    print("post guest session", data)


@pytest.mark.asyncio
async def test_guest_get_session(guest_get_session):
    data = guest_get_session
    print("get guest session", data)


@pytest.mark.asyncio
async def test_user_session_creation(user_session_creation):
    data = user_session_creation
    print("post user session", data)


@pytest.mark.asyncio
async def test_user_get_sessions(user_get_sessions):
    data = user_get_sessions
    print("get user session", data)


# def user_consent_gate_auth_test():
#     print("fn test")


# def guest_consent_gate_auth_test():
#     print("fn test")


# # * POST /auth/consent
# @pytest.mark.asyncio
# async def test_guest_flow(client: AsyncClient):
#     print("api test")


# # * POST /auth/guest-consent
# @pytest.mark.asyncio
# async def test_consent_flow(client: AsyncClient):
#     print("api test")
