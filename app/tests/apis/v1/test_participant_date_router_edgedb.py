import uuid

import httpx
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app import app
from app.utils.edgedb import edgedb_client


async def test_turn_on_participant_date() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-07",
            },
        )

        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": url_code,
            },
        )
        dates = create_participant_response.json()["participant_dates"]

        await client.patch(
            url="/v1/edgedb/participant_dates/off",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )

        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/on",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )
    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["participants"][0]["dates"][0]["enabled"] is True
    participant_date = await edgedb_client.query_single(
        f'select ParticipantDate {{enabled}} FILTER .id=<uuid>"{dates[0]["id"]}"'
    )
    assert participant_date.enabled is True


async def test_turn_on_participant_date_not_found() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            url="/v1/edgedb/participant_dates/on",
            json={
                "participant_date_id": str(uuid.uuid4()),
                "meeting_url_code": "not_found",
            },
        )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "meeting with url_code: not_found not found"}


async def test_turn_off_participant_date() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-07",
            },
        )

        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": url_code,
            },
        )
        dates = create_participant_response.json()["participant_dates"]

        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/off",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )
    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["participants"][0]["dates"][0]["enabled"] is False
    participant_date = await edgedb_client.query_single(
        f'select ParticipantDate {{enabled}} FILTER .id=<uuid>"{dates[0]["id"]}"'
    )
    assert participant_date.enabled is False


async def test_turn_off_participant_date_not_found() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            url="/v1/edgedb/participant_dates/off",
            json={
                "participant_date_id": str(uuid.uuid4()),
                "meeting_url_code": "not_found",
            },
        )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "meeting with url_code: not_found not found"}


async def test_star_participant_date() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-07",
            },
        )

        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": url_code,
            },
        )
        dates = create_participant_response.json()["participant_dates"]

        await client.patch(
            url="/v1/edgedb/participant_dates/off",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )

        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/star",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )

    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["participants"][0]["dates"][0]["starred"] is True
    assert response_body["participants"][0]["dates"][0]["enabled"] is True
    participant_date = await edgedb_client.query_single(
        f'select ParticipantDate {{starred, enabled}} FILTER .id=<uuid>"{dates[0]["id"]}"'
    )
    assert participant_date.starred is True
    assert participant_date.enabled is True


async def test_star_participant_date_when_meeting_does_not_exist() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/star",
            json={
                "participant_date_id": str(uuid.uuid4()),
                "meeting_url_code": "not_found",
            },
        )

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "meeting with url_code: not_found not found"}


async def test_unstar_participant_date() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-07",
            },
        )

        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": url_code,
            },
        )
        dates = create_participant_response.json()["participant_dates"]

        await client.patch(
            url="/v1/edgedb/participant_dates/star",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )

        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/unstar",
            json={
                "participant_date_id": dates[0]["id"],
                "meeting_url_code": url_code,
            },
        )

    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["participants"][0]["dates"][0]["starred"] is False
    participant_date = await edgedb_client.query_single(
        f'select ParticipantDate {{starred}} FILTER .id=<uuid>"{dates[0]["id"]}"'
    )
    assert participant_date.starred is False


async def test_unstar_participant_date_when_meeting_does_not_exist() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # When
        response = await client.patch(
            url="/v1/edgedb/participant_dates/unstar",
            json={
                "participant_date_id": str(uuid.uuid4()),
                "meeting_url_code": "not_found",
            },
        )

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "meeting with url_code: not_found not found"}
