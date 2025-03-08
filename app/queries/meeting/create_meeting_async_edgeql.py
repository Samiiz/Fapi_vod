import dataclasses
import uuid
from typing import cast

import edgedb


@dataclasses.dataclass(frozen=True)
class CreateMeetingResult:
    id: uuid.UUID
    url_code: str


async def create_meeting(
    executor: edgedb.AsyncIOExecutor,
    *,
    url_code: str,
) -> CreateMeetingResult:
    return cast(
        CreateMeetingResult,
        await executor.query_single(
            """\
        with
            url_code := <str>$url_code
        select (
            insert Meeting {
                url_code := url_code,
            }
        ) {url_code}\
        """,
            url_code=url_code,
        ),
    )
