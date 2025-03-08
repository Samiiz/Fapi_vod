import httpx
from starlette.status import HTTP_200_OK

from app import app
from app.utils.edgedb import edgedb_client


async def test_api_create_meeting_edgedb() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            url=f"/v1/edgedb/meetings",
        )

    assert response.status_code == HTTP_200_OK

    url_code = response.json()["url_code"]

    assert (
        await edgedb_client.query_single(
        f"select exists (select Meeting filter .url_code = '{url_code}')"
        )
    ) is True
