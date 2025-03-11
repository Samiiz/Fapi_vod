import asyncio
from typing import Generator

import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator[object]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
