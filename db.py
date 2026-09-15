import asyncpg

async def pool(dsn):
    result=await asyncpg.create_pool(dsn)
    return result

