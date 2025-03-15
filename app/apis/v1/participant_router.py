from fastapi import APIRouter, HTTPException
from starlette import status

from app.dtos.create_participant_request import CreateParticipantRequest
from app.dtos.create_participant_response import CreateParticipantEdgedbResponse
from app.services.meeting_service_edgedb import service_get_meeting_edgedb
from app.services.participant_service_edgedb import service_create_participant_edgedb

edgedb_router = APIRouter(prefix="/v1/edgedb/participants", tags=["Participant"])


@edgedb_router.post("", description="participant 를 생성합니다.")
async def api_create_participant_edgedb(
    create_participant_request: CreateParticipantRequest,
) -> CreateParticipantEdgedbResponse:
    meeting = await service_get_meeting_edgedb(create_participant_request.meeting_url_code)

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"meeting_url_code: {create_participant_request.meeting_url_code} 은 없습니다.",
        )

    if not (meeting.start_date and meeting.end_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="미팅의 시작일과 종료일이 모두 지정되어 있어야 합니다.",
        )

    participant, dates = await service_create_participant_edgedb(
        create_participant_request,
        meeting.start_date,
        meeting.end_date,
    )
    return CreateParticipantEdgedbResponse(participant_id=participant.id, participant_dates=dates)
