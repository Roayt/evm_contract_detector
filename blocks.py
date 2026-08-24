from rpc import get_latest_arc_block
import asyncio

async def get_latest_block(client):
    while True:
     block=await get_latest_arc_block(client)
     print(block)

     await asyncio.sleep(5)

