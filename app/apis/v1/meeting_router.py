from fastapi import APIRouter

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.services.meeting_service_edgedb import service_create_meeting_edgedb

edgedb_router = APIRouter(prefix="/v1/edgedb/meetings", tags=["Meeting"])
mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["Meeting"])


@edgedb_router.post("", description="meeting을 생성합니다.")
async def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_edgedb()).url_code)


@mysql_router.post("", description="meeting을 생성합니다.")
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abcasdasdasdads")
