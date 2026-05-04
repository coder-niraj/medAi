import pytest
from httpx import AsyncClient
from sqlalchemy import inspect

def image_only_routing_test():
    print("fn test")
    
def MIME_type_validation_via_magic_bytes():
    print("fn test")
    
def retention_expires_at_test():
    print("fn test")


# * POST /reports/upload
@pytest.mark.asyncio
async def test_guest_flow(client: AsyncClient):
    print("api test")
    
# * GET /reports
@pytest.mark.asyncio
async def test_guest_flow(client: AsyncClient):
    print("api test")

# * GET /reports/{id}/summary
@pytest.mark.asyncio
async def test_guest_flow(client: AsyncClient):
    print("api test")

# * GET /reports/{id}/file
@pytest.mark.asyncio
async def test_guest_flow(client: AsyncClient):
    print("api test")

# * DELETE /reports/{report_id}
@pytest.mark.asyncio
async def test_consent_flow(client: AsyncClient):
    print("api test")

