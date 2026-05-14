import asyncio
from http import client
from urllib import response

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch
from sqlalchemy import inspect
from main import fast_app
from uuid import uuid4

BASE_URL = "http://test"
CURRENT_REPORT_IDEMPOTENCY = "cef06506-0c6d-4c08-9f68-535ad79506ee"


# * POST /reports/upload
@pytest.fixture(scope="session")
async def report_upload_no_idempotency(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        with open("tests/files/test.png", "rb") as file_data:
            response = await client.post(
                "/reports/upload",
                headers={"Authorization": f"bearer {JWT_consent_token}"},
                files={
                    "file": (
                        "test.pdf",
                        file_data,
                        "application/pdf",
                    )
                },
                data={
                    "report_type": "cbc",
                    "display_name": "ancs",
                },
            )

        return response.status_code


@pytest.mark.asyncio
async def test_report_no_idempotency(report_upload_no_idempotency):
    assert report_upload_no_idempotency == 400
