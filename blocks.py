from rpc import get_latest_arc_block,gets_block,get_contract
import time 
import asyncio
from last_seen import write_last_seen,read_last_seen
import logging
logger=logging.getLogger(__name__)

async def get_latest_block(client):

    try:
        nums=read_last_seen()

        if nums is None:
            logger.error("stored file returned None object so using default caller")
            t=await get_latest_arc_block(client)
            if t is None:
                raise ValueError("Im receiving none object")   
            last_seen=int(t,16)
        else:
            last_seen=nums
        while True:
            try:
                num=await get_latest_arc_block(client)
                code=int(num,16)
            except Exception as e:
                logger.warning(f"couldn't fetch the block height,trying again: {e}")
                await asyncio.sleep(2)
                continue     

            for i in range(last_seen +1,code+1):
                blocknum=(hex(i))

                result= await gets_block(client,blocknum)
                if result is None:
                    logger.error("Received None object continuine back the loop")
                    await asyncio.sleep(5)
                    continue                                                
                           
                for txs in result:
                    if txs["to"] is  None:
                        result2= await get_contract(client,txs)
                        if result2 is None:
                            logger.warning("received None from Nodes,may receipt not available the moment")
                            continue 
                        
                        logger.info(f"Contract Address is {result2}")
                last_seen=code

              
                write_last_seen(i)

            await asyncio.sleep(2)

    except Exception as e:
        logger.error(f"Response from Rpc is broken: {e}")
