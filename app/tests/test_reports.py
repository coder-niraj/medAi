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
async def report_upload_image(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        with open("tests/files/test.png", "rb") as file_data:
            response = await client.post(
                "/reports/upload",
                headers={
                    "Authorization": f"bearer {JWT_consent_token}",
                    "Idempotency-Key": CURRENT_REPORT_IDEMPOTENCY,
                },
                files={
                    "file": (
                        "test.pdf",
                        file_data,
                        "image/png",
                    )
                },
                data={
                    "report_type": "cbc",
                    "display_name": "ancs",
                },
            )
        assert response.status_code in [200, 202, 201]
        body = response.json()
        return body


# * DELETE /reports/{:id}
@pytest.fixture(scope="session")
async def report_delete(report_upload_image, JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.delete(
            "/reports/" + report_upload_image["report_id"],
            headers={
                "Authorization": f"bearer {JWT_consent_token}",
            },
        )
        return response.status_code


# * POST /reports/
@pytest.fixture(scope="session")
async def report_list(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        with open("tests/files/test.png", "rb") as file_data:
            response = await client.get(
                "/reports/",
                headers={
                    "Authorization": f"bearer {JWT_consent_token}",
                },
            )

        return response.status_code


# * POST /reports/upload
@pytest.fixture(scope="session")
async def report_upload_pdf(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        with open("tests/files/test.pdf", "rb") as file_data:
            response = await client.post(
                "/reports/upload",
                headers={
                    "Authorization": f"bearer {JWT_consent_token}",
                    "Idempotency-Key": str(uuid4()),
                },
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
        assert response.status_code == 200
        body = response.json()
        return body


# * POST /reports/upload
@pytest.fixture(scope="session")
async def report_validation(JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/reports/upload",
            headers={
                "Authorization": f"bearer {JWT_consent_token}",
                "Idempotency-Key": str(uuid4()),
            },
            data={
                "report_type": "cbc",
                "display_name": "ancs",
            },
        )
        body = response.json()
        return response.status_code


# * POST /reports/upload
@pytest.fixture(scope="session")
async def report_upload_no_jwt():
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        with open("tests/files/test.png", "rb") as file_data:
            response = await client.post(
                "/reports/upload",
                headers={
                    "Idempotency-Key": str(uuid4()),
                },
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


# * GET /reports/{:id}
@pytest.fixture(scope="session")
async def report_get_url(report_upload_image, JWT_consent_token):
    async with AsyncClient(
        transport=ASGITransport(app=fast_app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/reports/" + report_upload_image["report_id"] + "/file",
            headers={
                "Authorization": f"bearer {JWT_consent_token}",
            },
        )
        return response.status_code


@pytest.mark.asyncio
async def test_report_upload_png(report_upload_image):
    keys_to_check = [
        "report_id",
        "status",
        "Message_ar",
        "Message_en",
    ]
    result = all(k in report_upload_image for k in keys_to_check)
    assert result == True
    #


@pytest.mark.asyncio
async def test_report_upload_pdf(report_upload_pdf):
    keys_to_check = [
        "report_id",
        "status",
    ]
    result = all(k in report_upload_pdf for k in keys_to_check)
    assert result == True


@pytest.mark.asyncio
async def test_report_validation(report_validation):
    assert report_validation == 422


@pytest.mark.asyncio
async def test_report_no_jwt(report_upload_no_jwt):
    assert report_upload_no_jwt in [403, 401]


@pytest.mark.asyncio
async def test_report_list(report_list):
    assert report_list in [200, 202]


@pytest.mark.asyncio
async def test_report_get_url(report_get_url):
    assert report_get_url in [200, 404, 500]


@pytest.mark.asyncio
async def test_report_delete(report_delete):
    assert report_delete in [200, 404, 422]


# # * GET /reports/{id}/summary
# @pytest.mark.asyncio
# async def test_guest_flow(client: AsyncClient):
#     print("api test")


# # * GET /reports/{id}/file
# @pytest.mark.asyncio
# async def test_guest_flow(client: AsyncClient):
#     print("api test")

# def image_only_routing_test():
#     print("fn test")


# def MIME_type_validation_via_magic_bytes():
#     print("fn test")


# def retention_expires_at_test():
#     print("fn test")
