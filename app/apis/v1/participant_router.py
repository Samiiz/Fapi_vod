import uuid

from fastapi import APIRouter

from app.dtos.create_participant_request import CreateParticipantRequest
from app.dtos.create_participant_response import CreateParticipantEdgedbResponse

edgedb_router = APIRouter(prefix="/v1/edgedb/participants", tags=["Participant"])


@edgedb_router.post("", description="participant를 생성합니다.")
async def api_create_participant_edgedb(
    create_participant_request: CreateParticipantRequest,
) -> CreateParticipantEdgedbResponse:
    return CreateParticipantEdgedbResponse(participant_id=uuid.uuid4(), participant_dates=[])
