from datetime import date, timedelta

from app.dtos.create_participant_request import CreateParticipantRequest
from app.dtos.create_participant_response import ParticipantDateEdgedb
from app.queries.participant.create_participant_with_dates_async_edgeql import (
    CreateParticipantWithDatesResultParticipant,
    create_participant_with_dates,
)
from app.utils.edgedb import edgedb_client


async def service_create_participant_edgedb(
    create_participant_request: CreateParticipantRequest,
    meeting_start_date: date,
    meeting_end_date: date,
) -> tuple[CreateParticipantWithDatesResultParticipant, list[ParticipantDateEdgedb]]:
    default_dates = [
        meeting_start_date + timedelta(days=i) for i in range((meeting_end_date - meeting_start_date).days + 1)
    ]
    dates_result = await create_participant_with_dates(
        edgedb_client,
        name=create_participant_request.name,
        url_code=create_participant_request.meeting_url_code,
        dates=default_dates,
    )
    return dates_result[0].participant, [
        ParticipantDateEdgedb(id=id_, date=date) for id_, date in zip([date.id for date in dates_result], default_dates)
    ]
