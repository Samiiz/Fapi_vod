import datetime

import httpx
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app import app
from app.dtos.update_meeting_request import MEETING_DATE_MAX_RANGE
from app.utils.edgedb import edgedb_client


async def test_api_create_meeting_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            url="/v1/edgedb/meetings",
        )

    assert response.status_code == HTTP_200_OK

    url_code = response.json()["url_code"]

    assert (
        await edgedb_client.query_single(f"select exists (select Meeting filter .url_code = '{url_code}');")
    ) is True


async def test_api_get_meeting() -> None:
    # Given
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": (start_date := "2025-12-01"),
                "end_date": (end_date := "2025-12-04"),
            },
        )

        await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": (participant_name := "tester_hoon"),
                "meeting_url_code": url_code,
            },
        )

        await client.patch(f"/v1/edgedb/meetings/{url_code}/title", json={"title": (title := "abc")})

        # When
        response = await client.get(url=f"/v1/edgedb/meetings/{url_code}")

    # Then
    assert response.status_code == HTTP_200_OK
    response_body = response.json()
    assert response_body["url_code"] == url_code
    assert response_body["start_date"] == start_date
    assert response_body["end_date"] == end_date
    assert response_body["title"] == title
    assert response_body["location"] == ""
    assert len(response_body["participants"]) == 1
    participant = response_body["participants"][0]
    assert participant["name"] == participant_name
    assert [date["date"] for date in participant["dates"]] == [
        "2025-12-01",
        "2025-12-02",
        "2025-12-03",
        "2025-12-04",
    ]


async def test_api_get_meeting_404() -> None:
    # Given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # When
        response = await client.get(
            url="/v1/edgedb/meetings/invalid_url",
        )

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "meeting with url_code: invalid_url not found"


async def test_api_update_meeting_date_range_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        response = await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={"start_date": "2025-10-10", "end_date": "2025-10-20"},
        )

    assert response.status_code == HTTP_200_OK
    response_body = response.json()

    assert response_body["start_date"] == "2025-10-10"
    assert response_body["end_date"] == "2025-10-20"

    meeting = await edgedb_client.query_single(
        f"select Meeting {{start_date, end_date}} filter .url_code = '{url_code}';"
    )
    assert meeting.start_date == datetime.date(2025, 10, 10)
    assert meeting.end_date == datetime.date(2025, 10, 20)


async def test_can_not_update_meeting_date_range_when_range_is_too_long_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        response = await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={"start_date": (start := "2025-10-10"), "end_date": (end := "2030-10-20")},
        )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    response_body = response.json()
    assert (
        response_body["detail"]
        == f"start_date: {start} and end_date: {end} should be within {MEETING_DATE_MAX_RANGE.days} days"
    )


async def test_can_not_update_meeting_date_range_when_it_is_already_set_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={"start_date": "2025-10-12", "end_date": "2025-10-22"},
        )

        response = await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={"start_date": "2025-10-12", "end_date": "2025-10-22"},
        )

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    response_body = response.json()
    assert response_body["detail"] == f"meeting: {url_code} start_date: 2025-10-12 end_date: 2025-10-22 are already set"


async def test_can_not_update_meeting_does_not_exists_edgedb() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:

        url_code = "invalid_url"

        response = await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={"start_date": "2025-10-12", "end_date": "2025-10-22"},
        )

    assert response.status_code == HTTP_404_NOT_FOUND
    response_body = response.json()
    assert response_body["detail"] == "meeting with url_code: invalid_url not found"


async def test_api_update_meeting_title_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        response = await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/title",
            json={"title": (title := "new title")},
        )

    assert response.status_code == HTTP_204_NO_CONTENT
    meeting = await edgedb_client.query_single(f"select Meeting {{title}} filter .url_code = '{url_code}';")
    assert meeting.title == title


async def test_can_not_update_meeting_title_when_meeting_does_not_exists() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:

        url_code = "invalid_url_code"

        # When
        response = await client.patch(f"/v1/edgedb/meetings/{url_code}/title", json={"title": "abc"})

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND


async def test_api_update_meeting_location() -> None:
    # given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_meeting_response = await client.post(url="/v1/edgedb/meetings")
        url_code = create_meeting_response.json()["url_code"]
        location = "test location"

        # when
        response = await client.patch(f"/v1/edgedb/meetings/{url_code}/location", json={"location": location})

    # then
    assert response.status_code == HTTP_204_NO_CONTENT


async def test_can_not_update_meeting_location_when_meeting_does_not_exists() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        url_code = "invalid_url_code"

        # When
        response = await client.patch(f"/v1/edgedb/meetings/{url_code}/location", json={"location": "abc"})

    # Then
    assert response.status_code == HTTP_404_NOT_FOUND
