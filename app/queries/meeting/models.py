import dataclasses
import uuid
from datetime import date


@dataclasses.dataclass(frozen=True)
class ParticipantDate:
    id: uuid.UUID
    date: date
    starred: bool
    enabled: bool


@dataclasses.dataclass(frozen=True)
class Participant:
    id: uuid.UUID
    name: str
    dates: list[ParticipantDate]


@dataclasses.dataclass(frozen=True)
class FullMeeting:
    url_code: str
    start_date: date | None
    end_date: date | None
    location: str
    title: str
    participants: list[Participant]
