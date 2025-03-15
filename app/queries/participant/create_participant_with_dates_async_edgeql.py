# AUTOGENERATED FROM 'app/queries/temp/create_participant_with_dates.edgeql' WITH:
#     $ edgedb-py --dir app/queries/temp --no-skip-pydantic-validation


from __future__ import annotations

import dataclasses
import datetime
import uuid
from typing import cast

import edgedb


@dataclasses.dataclass
class CreateParticipantWithDatesResult:
    id: uuid.UUID
    participant: CreateParticipantWithDatesResultParticipant


@dataclasses.dataclass
class CreateParticipantWithDatesResultParticipant:
    id: uuid.UUID


async def create_participant_with_dates(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
    url_code: str,
    dates: list[datetime.date],
) -> list[CreateParticipantWithDatesResult]:
    return cast(
        list[CreateParticipantWithDatesResult],
        await executor.query(
            """\
        with
            name := <str>$name,
            url_code := <str>$url_code,
            dates := <array<cal::local_date>>$dates,
            PARTICIPANT := (
                insert Participant {
                    name := name,
                    meeting := (
                        select Meeting
                        filter .url_code = url_code
                    )
                }
            ),
            DATES := (
                for date in array_unpack(dates)
                insert ParticipantDate {
                  participant := PARTICIPANT,
                  date := date,
                }
            ),
        select DATES {id, participant};\
        """,
            name=name,
            url_code=url_code,
            dates=dates,
        ),
    )
