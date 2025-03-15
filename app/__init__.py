from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.apis.v1.meeting_router import edgedb_router as meeting_edgedb_router
from app.apis.v1.participant_date_router import edgedb_router as participant_date_router
from app.apis.v1.participant_router import edgedb_router as participant_edgedb_router

app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.include_router(meeting_edgedb_router)
app.include_router(participant_edgedb_router)
app.include_router(participant_date_router)
