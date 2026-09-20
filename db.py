import asyncpg
import logging
logger=logging.getLogger(__name__)

async def pool(dsn):
    result=await asyncpg.create_pool(dsn)
    return result

async def insert_data(db_pool,contract_address,chain,symbol,blocknumber,deployer_address):
     try:
        sql="INSERT INTO contract(contract_address,chain,symbol,blocknumber,deployer_address) VALUES($1,$2,$3,$4,$5) ON CONFLICT DO NOTHING"
        return await db_pool.execute(sql,contract_address,chain,symbol,blocknumber,deployer_address)

     except Exception:
        logger.exception("Insert got failed for %s", contract_address) 
        return None

async def get_last_processed_block(db_pool,chain):

    try:
        sql= "SELECT last_processed_block FROM check_point WHERE chain=$1"
        return await db_pool.fetchval(sql,chain)

    except Exception:
        logger.exception("SELECT got failed for %s",chain)
