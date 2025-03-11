# import asyncio
# from typing import Generator
#
# import pytest_asyncio
#
#
# @pytest_asyncio.fixture(scope="session")
# def event_loop() -> Generator[object]:
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()
