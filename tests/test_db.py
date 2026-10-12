import asyncio

import pytest

from db import get_last_processed_block


class FakePool:
    async def fetchval(self, query, chain):
        raise ConnectionError("Database connection failed")


def test_checkpoint_read_raise_connection_error():
    with pytest.raises(ConnectionError):
        asyncio.run(get_last_processed_block(FakePool(), 1))
