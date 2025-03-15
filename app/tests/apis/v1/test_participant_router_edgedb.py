import datetime

import httpx
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app import app
from app.utils.edgedb import edgedb_client


async def test_create_participant_edgedb() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:

        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-04",
            },
        )

        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": (name := "tester-hoon"),
                "meeting_url_code": url_code,
            },
        )

        assert create_participant_response.status_code == HTTP_200_OK
        create_participant_response_body = create_participant_response.json()

        assert create_participant_response_body["participant_id"] is not None
        assert [date["date"] for date in create_participant_response_body["participant_dates"]] == [
            "2025-12-01",
            "2025-12-02",
            "2025-12-03",
            "2025-12-04",
        ]

        participant = await edgedb_client.query_single(
            f"SELECT Participant {{name, meeting_url_code:=.meeting.url_code}} FILTER .id=<uuid>'{create_participant_response_body["participant_id"]}'"
        )

        assert participant.name == name
        assert participant.meeting_url_code == url_code

        participant_dates = await edgedb_client.query(
            f"SELECT ParticipantDate {{date}} FILTER .participant.id=<uuid>'{create_participant_response_body["participant_id"]}'"
        )

        assert [date.date for date in participant_dates] == [
            datetime.date(2025, 12, 1),
            datetime.date(2025, 12, 2),
            datetime.date(2025, 12, 3),
            datetime.date(2025, 12, 4),
        ]


async def test_can_not_create_participant_meeting_not_found() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": "not_found",
            },
        )

    assert create_participant_response.status_code == HTTP_404_NOT_FOUND
    assert create_participant_response.json() == {"detail": "meeting_url_code: not_found 은 없습니다."}


async def test_can_not_create_participant_meeting_range_not_set() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Given
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        # When
        create_participant_response = await client.post(
            url="/v1/edgedb/participants",
            json={
                "name": "test_name",
                "meeting_url_code": url_code,
            },
        )
    # Then
    assert create_participant_response.status_code == HTTP_400_BAD_REQUEST
    assert create_participant_response.json() == {"detail": "미팅의 시작일과 종료일이 모두 지정되어 있어야 합니다."}
