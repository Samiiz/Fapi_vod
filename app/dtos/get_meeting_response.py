import uuid
from datetime import date

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class ParticipantDateResponse(BaseModel):
    model_config = FROZEN_CONFIG
    date: date
    id: uuid.UUID | int


class ParticipantResponse(BaseModel):
    model_config = FROZEN_CONFIG
    id: uuid.UUID | int
    name: str
    dates: list[ParticipantDateResponse]


class GetMeetingResponse(BaseModel):
    model_config = FROZEN_CONFIG

    url_code: str
    start_date: date | None = None
    end_date: date | None = None
    title: str
    location: str
    participants: list[ParticipantResponse]
