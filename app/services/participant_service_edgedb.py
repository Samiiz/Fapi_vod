from datetime import date, timedelta

from app.dtos.create_participant_request import CreateParticipantRequest
from app.dtos.create_participant_response import ParticipantDateEdgedb
from app.queries.participant.bulk_create_participant_date_async_edgeql import (
    bulk_create_participant_date,
)
from app.queries.participant.create_participant_async_edgeql import (
    CreateParticipantResult,
    create_participant,
)
from app.utils.edgedb import edgedb_client


async def service_create_participant_edgedb(
    create_participant_request: CreateParticipantRequest,
    meeting_start_date: date,
    meeting_end_date: date,
) -> tuple[CreateParticipantResult, list[ParticipantDateEdgedb]]:
    default_dates = [
        meeting_start_date + timedelta(days=i) for i in range((meeting_end_date - meeting_start_date).days + 1)
    ]
    async for tx in edgedb_client.transaction():
        async with tx:
            participant = await create_participant(
                tx,
                name=create_participant_request.name,
                url_code=create_participant_request.meeting_url_code,
            )
            dates_result = await bulk_create_participant_date(
                tx,
                participant_id=participant.id,
                dates=default_dates,
            )
    return participant, [
        ParticipantDateEdgedb(id=id_, date=date) for id_, date in zip([date.id for date in dates_result], default_dates)
    ]
