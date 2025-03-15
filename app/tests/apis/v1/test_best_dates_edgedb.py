import asyncio

import httpx
from starlette.status import HTTP_200_OK

from app import app
from app.utils.edgedb import edgedb_client


async def test_best_dates() -> None:
    """
    미팅 생성 -> 날짜 지정 -> 참가자 둘 생성

    2025-12-03 을 2명이 전부 켠다.
    2025-12-10 을 2명이 전부 켜고 1명이 스타 준다.
    2025-12-11 을 1명만 켠다.

    2명 모두 다 되고, 스타도 있는 12-10 이 1등,
    그 다음 12-03, 그 다음 12-11 순이다.
    """

    # Given
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_meeting_response = await client.post(
            url="/v1/edgedb/meetings",
        )
        url_code = create_meeting_response.json()["url_code"]

        await client.patch(
            url=f"/v1/edgedb/meetings/{url_code}/date_range",
            json={
                "start_date": "2025-12-01",
                "end_date": "2025-12-31",
            },
        )
        participant_response1, participant_response2 = await asyncio.gather(
            client.post(
                url="/v1/edgedb/participants",
                json={
                    "name": "test_name1",
                    "meeting_url_code": url_code,
                },
            ),
            client.post(
                url="/v1/edgedb/participants",
                json={
                    "name": "test_name2",
                    "meeting_url_code": url_code,
                },
            ),
        )

        participant_response1_body = participant_response1.json()
        participant_response2_body = participant_response2.json()
        participant1_id = participant_response1_body["participant_id"]
        participant2_id = participant_response2_body["participant_id"]

        await edgedb_client.execute(
            f"UPDATE ParticipantDate FILTER .participant.id = <uuid>'{participant1_id}' SET " + "{enabled := false}"
        )
        await edgedb_client.execute(
            f"UPDATE ParticipantDate FILTER .participant.id = <uuid>'{participant2_id}' SET " + "{enabled := false}"
        )

        await asyncio.gather(
            client.patch(
                url="/v1/edgedb/participant_dates/on",
                json={
                    "participant_date_id": participant_response1_body["participant_dates"][2]["id"],
                    "meeting_url_code": url_code,
                },
            ),
            client.patch(
                url="/v1/edgedb/participant_dates/on",
                json={
                    "participant_date_id": participant_response2_body["participant_dates"][2]["id"],
                    "meeting_url_code": url_code,
                },
            ),
            client.patch(
                url="/v1/edgedb/participant_dates/on",
                json={
                    "participant_date_id": participant_response1_body["participant_dates"][10]["id"],
                    "meeting_url_code": url_code,
                },
            ),
            client.patch(
                url="/v1/edgedb/participant_dates/on",
                json={
                    "participant_date_id": participant_response2_body["participant_dates"][9]["id"],
                    "meeting_url_code": url_code,
                },
            ),
            client.patch(
                url="/v1/edgedb/participant_dates/on",
                json={
                    "participant_date_id": participant_response1_body["participant_dates"][9]["id"],
                    "meeting_url_code": url_code,
                },
            ),
        )

        await client.patch(
            url="/v1/edgedb/participant_dates/star",
            json={
                "participant_date_id": participant_response1_body["participant_dates"][9]["id"],
                "meeting_url_code": url_code,
            },
        )

        meeting_response = await client.get(
            url=f"/v1/edgedb/meetings/{url_code}",
        )

    assert meeting_response.status_code == HTTP_200_OK
    meeting_response_body = meeting_response.json()
    assert meeting_response_body["best_dates"] == ["2025-12-10", "2025-12-03", "2025-12-11"]
