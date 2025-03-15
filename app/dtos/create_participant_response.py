import datetime
import uuid

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class ParticipantDateEdgedb(BaseModel):
    model_config = FROZEN_CONFIG
    id: uuid.UUID
    date: datetime.date


class CreateParticipantEdgedbResponse(BaseModel):
    model_config = FROZEN_CONFIG
    participant_id: uuid.UUID
    participant_dates: list[ParticipantDateEdgedb]
