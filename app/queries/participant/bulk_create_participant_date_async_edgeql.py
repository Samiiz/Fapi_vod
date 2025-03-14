# AUTOGENERATED FROM 'app/queries/participant/bulk_create_participant_date.edgeql' WITH:
#     $ edgedb-py --dir app/queries/participant --no-skip-pydantic-validation


from __future__ import annotations

import dataclasses
import datetime
import uuid
from typing import cast

import edgedb


@dataclasses.dataclass
class BulkCreateParticipantDateResult:
    id: uuid.UUID


async def bulk_create_participant_date(
    executor: edgedb.AsyncIOExecutor,
    *,
    participant_id: uuid.UUID,
    dates: list[datetime.date],
) -> list[BulkCreateParticipantDateResult]:
    return cast(
        list[BulkCreateParticipantDateResult],
        await executor.query(
            """\
        with
            participant_id := <uuid>$participant_id,
            dates := <array<cal::local_date>>$dates
        for date in array_unpack(dates) union (
            insert ParticipantDate {
                participant := <Participant>participant_id,
                date := date,
            }
        )\
        """,
            participant_id=participant_id,
            dates=dates,
        ),
    )
