# AUTOGENERATED FROM 'app/queries/meeting/get_meeting_by_url_code.edgeql' WITH:
#     $ edgedb-py --dir app/queries/meeting --no-skip-pydantic-validation


from __future__ import annotations

from typing import cast

import edgedb

from app.queries.meeting.models import FullMeeting


async def get_meeting_by_url_code(
    executor: edgedb.AsyncIOExecutor,
    *,
    url_code: str,
) -> FullMeeting | None:
    return cast(
        FullMeeting | None,
        await executor.query_single(
            """\
        with
            url_code := <str>$url_code,
        select Meeting { url_code }
        filter .url_code = url_code
        limit 1\
        """,
            url_code=url_code,
        ),
    )
