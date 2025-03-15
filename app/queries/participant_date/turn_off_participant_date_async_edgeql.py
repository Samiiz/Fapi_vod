# AUTOGENERATED FROM 'app/queries/participant_date/turn_off_participant_date.edgeql' WITH:
#     $ edgedb-py --dir app/queries/participant_date --no-skip-pydantic-validation


from __future__ import annotations

import dataclasses
import uuid
from typing import cast

import edgedb


@dataclasses.dataclass
class TurnOffParticipantDateResult:
    id: uuid.UUID


async def turn_off_participant_date(
    executor: edgedb.AsyncIOExecutor,
    *,
    participant_date_id: uuid.UUID,
) -> TurnOffParticipantDateResult | None:
    return cast(
        TurnOffParticipantDateResult | None,
        await executor.query_single(
            """\
        with
            participant_date_id := <uuid>$participant_date_id,
        update ParticipantDate
        filter .id = participant_date_id
        set {enabled := false, starred := false};\
        """,
            participant_date_id=participant_date_id,
        ),
    )
