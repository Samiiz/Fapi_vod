import uuid

from app.queries.participant_date.star_async_edgeql import star
from app.queries.participant_date.turn_off_participant_date_async_edgeql import (
    turn_off_participant_date,
)
from app.queries.participant_date.turn_on_participant_date_async_edgeql import (
    turn_on_participant_date,
)
from app.queries.participant_date.unstar_async_edgeql import unstar
from app.utils.edgedb import edgedb_client


async def service_turn_on_participant_date_edgedb(
    participant_date_id: uuid.UUID,
) -> None:
    await turn_on_participant_date(
        edgedb_client,
        participant_date_id=participant_date_id,
    )


async def service_turn_off_participant_date_edgedb(
    participant_date_id: uuid.UUID,
) -> None:
    await turn_off_participant_date(
        edgedb_client,
        participant_date_id=participant_date_id,
    )


async def service_star_participant_date_edgedb(
    participant_date_id: uuid.UUID,
) -> None:
    await star(
        edgedb_client,
        participant_date_id=participant_date_id,
    )


async def service_unstar_participant_date_edgedb(
    participant_date_id: uuid.UUID,
) -> None:
    await unstar(
        edgedb_client,
        participant_date_id=participant_date_id,
    )
