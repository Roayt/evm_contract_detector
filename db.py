import asyncpg
import logging
logger=logging.getLogger(__name__)

async def pool(dsn):
    result=await asyncpg.create_pool(dsn)
    return result

async def insert_data(db_pool,address,chain,symbol,blocknumber,deployer):
     try:
        sql="INSERT INTO contract(address,chain,symbol,blocknumber,deployer) VALUES($1,$2,$3,$4,$5) ON CONFLICT DO NOTHING"
        return await db_pool.execute(sql,address,chain,symbol,blocknumber,deployer)

     except Exception:
         return logger.exception("Failed to get chainId")
