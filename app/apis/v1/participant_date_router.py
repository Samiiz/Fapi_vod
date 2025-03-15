from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.dtos.get_meeting_response import (
    GetMeetingResponse,
)
from app.dtos.turn_on_off_star_participant_date_request import (
    TurnOnOffStarParticipantDateRequestEdgedb,
)
from app.services.meeting_service_edgedb import (
    service_get_meeting_edgedb,
)
from app.services.participant_date_service_edgedb import (
    service_star_participant_date_edgedb,
    service_turn_off_participant_date_edgedb,
    service_turn_on_participant_date_edgedb,
    service_unstar_participant_date_edgedb,
)

edgedb_router = APIRouter(prefix="/v1/edgedb/participant_dates", tags=["ParticipantDate"])


@edgedb_router.patch(
    "/on",
    description="특정 참가자의 특정 날짜를 켭니다.",
)
async def api_turn_on_date_edgedb(
    turn_on_participant_day_request: TurnOnOffStarParticipantDateRequestEdgedb,
) -> GetMeetingResponse:
    await service_turn_on_participant_date_edgedb(turn_on_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_edgedb(turn_on_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {turn_on_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_edgedb(meeting)


@edgedb_router.patch(
    "/off",
    description="특정 참가자의 특정 날짜를 끕니다.",
)
async def api_turn_off_date_edgedb(
    turn_off_participant_day_request: TurnOnOffStarParticipantDateRequestEdgedb,
) -> GetMeetingResponse:
    await service_turn_off_participant_date_edgedb(turn_off_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_edgedb(turn_off_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {turn_off_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_edgedb(meeting)


@edgedb_router.patch(
    "/star",
    description="특정 참가자의 특정 날짜를 별표로 표시합니다.",
)
async def api_star_date_edgedb(
    star_participant_day_request: TurnOnOffStarParticipantDateRequestEdgedb,
) -> GetMeetingResponse:
    await service_star_participant_date_edgedb(star_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_edgedb(star_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {star_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_edgedb(meeting)


@edgedb_router.patch(
    "/unstar",
    description="특정 참가자의 특정 날짜의 별을 제거합니다.",
)
async def api_unstar_date_edgedb(
    unstar_participant_day_request: TurnOnOffStarParticipantDateRequestEdgedb,
) -> GetMeetingResponse:
    await service_unstar_participant_date_edgedb(unstar_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_edgedb(unstar_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {unstar_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_edgedb(meeting)
