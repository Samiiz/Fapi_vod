# AUTOGENERATED FROM 'app/queries/participant/create_participant.edgeql' WITH:
#     $ edgedb-py --dir app/queries/participant --no-skip-pydantic-validation


from __future__ import annotations

import dataclasses
import uuid
from typing import cast

import edgedb


@dataclasses.dataclass
class CreateParticipantResult:
    id: uuid.UUID


async def create_participant(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
    url_code: str,
) -> CreateParticipantResult:
    return cast(
        CreateParticipantResult,
        await executor.query_single(
            """\
        with
            name := <str>$name,
            url_code := <str>$url_code,
        insert Participant {
            name := name,
            meeting := (
                select Meeting
                filter .url_code = url_code
            )
        }\
        """,
            name=name,
            url_code=url_code,
        ),
    )
