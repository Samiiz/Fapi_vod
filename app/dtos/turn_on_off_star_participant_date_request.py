import uuid

from pydantic import BaseModel


class TurnOnOffStarParticipantDateRequestEdgedb(BaseModel):
    participant_date_id: uuid.UUID
    meeting_url_code: str
