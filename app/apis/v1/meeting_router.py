from datetime import datetime

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.dtos.update_meeting_request import UpdateMeetingDateRangeRequest
from app.services.meeting_service_edgedb import (
    service_create_meeting_edgedb,
    service_get_meeting_edgedb,
)

edgedb_router = APIRouter(prefix="/v1/edgedb/meetings", tags=["Meeting"])
mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["Meeting"])


@edgedb_router.post("", description="meeting을 생성합니다.")
async def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_edgedb()).url_code)


@edgedb_router.get(
    "/{meeting_url_code}",
    description="meeting 을 조회합니다.",
)
async def api_get_meeting_edgedb(meeting_url_code: str) -> GetMeetingResponse:
    meeting = await service_get_meeting_edgedb(meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"meeting with url_code: {meeting_url_code} not found"
        )
    return GetMeetingResponse(
        url_code=meeting.url_code,
        end_date=datetime.now().date(),
        start_date=datetime.now().date(),
        title="test",
        location="test",
    )


@edgedb_router.patch("/{meeting_url_code}/date_range", description="Meeting을 수정합니다.")
async def api_update_meeting_date_range_edgdb(
    meeting_url_code: str, update_meetin_date_range_request: UpdateMeetingDateRangeRequest
) -> GetMeetingResponse:
    return GetMeetingResponse(
        url_code="abc",
        end_date=datetime.now().date(),
        start_date=datetime.now().date(),
        title="test",
        location="test",
    )


# @mysql_router.post("", description="meeting을 생성합니다.")
# async def api_create_meeting_mysql() -> CreateMeetingResponse:
#     return CreateMeetingResponse(url_code="abcasdasdasdads")
