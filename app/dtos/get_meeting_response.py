from __future__ import annotations

import dataclasses
import uuid
from datetime import date
from typing import Iterable

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG
from app.queries.meeting.models import FullMeeting, ParticipantDate


@dataclasses.dataclass
class BestDate:
    date: date
    enable_count: int
    star_count: int


class ParticipantDateResponse(BaseModel):
    model_config = FROZEN_CONFIG
    date: date
    id: uuid.UUID | int
    enabled: bool
    starred: bool


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
    best_dates: list[date]

    @classmethod
    def from_edgedb(cls, meeting: FullMeeting) -> GetMeetingResponse:
        return GetMeetingResponse(
            url_code=meeting.url_code,
            start_date=meeting.start_date,
            end_date=meeting.end_date,
            title=meeting.title,
            location=meeting.location,
            participants=[
                ParticipantResponse(
                    id=participant.id,
                    name=participant.name,
                    dates=[
                        ParticipantDateResponse(
                            id=participant_date.id,
                            date=participant_date.date,
                            enabled=participant_date.enabled,
                            starred=participant_date.starred,
                        )
                        for participant_date in participant.dates
                    ],
                )
                for participant in meeting.participants
            ],
            best_dates=cls._get_best_dates(
                (participant_date for participant in meeting.participants for participant_date in participant.dates)
            ),
        )

    @classmethod
    def _get_best_dates(cls, participant_dates: Iterable[ParticipantDate]) -> list[date]:
        result_dict: dict[date, BestDate] = {}

        for participant_date in participant_dates:
            if participant_date.date not in result_dict:
                result_dict[participant_date.date] = BestDate(
                    date=participant_date.date,
                    enable_count=0,
                    star_count=0,
                )
            if participant_date.enabled:
                result_dict[participant_date.date].enable_count += 1
                if participant_date.starred:
                    result_dict[participant_date.date].star_count += 1

        result_list = list(result_dict.values())
        result_list.sort(
            key=lambda best_date: (
                -best_date.enable_count,
                -best_date.star_count,
                best_date.date,
            ),
        )
        return [best_date.date for best_date in result_list[:3]]
