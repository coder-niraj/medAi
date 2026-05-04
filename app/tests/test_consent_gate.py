import pytest
from httpx import AsyncClient
from sqlalchemy import inspect

def user_consent_gate_auth_test():
    print("fn test")
    
def guest_consent_gate_auth_test():
    print("fn test")


# * POST /auth/consent
@pytest.mark.asyncio
async def test_guest_flow(client: AsyncClient):
    print("api test")

# * POST /auth/guest-consent
@pytest.mark.asyncio
async def test_consent_flow(client: AsyncClient):
    print("api test")

