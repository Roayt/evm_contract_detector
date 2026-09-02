from rpc import get_latest_arc_block,gets_block,get_contract,get_symbol
import asyncio
from last_seen import write_last_seen,read_last_seen
import logging
logger=logging.getLogger(__name__)

async def get_latest_block(client,url,time,block_height):

    try:

        nums=read_last_seen()
        if nums is None:
            logger.error("stored file returned None object so using default caller")

            t=await get_latest_arc_block(client,url)
            if t is None:
                raise ValueError("Im receiving none object") 
            last_seen=int(t,16)


        else:
            last_seen=nums

        if block_height:
                    last_seen=block_height
 

        while True:
            try:
                num=await get_latest_arc_block(client,url)
                code=int(num,16)
            except Exception as e:
                logger.warning(f"couldn't fetch the block height,trying again: {e}")
                await asyncio.sleep(time)
                continue     

            for i in range(last_seen +1,code+1):
                blocknum=(hex(i))

                result= await gets_block(client,blocknum,url)
                if result is None:
                    logger.error("Received None object continuine back the loop")
                    await asyncio.sleep(time)
                    continue                                                
                           
                for txs in result:
                    if txs["to"] is  None:
                        result2= await get_contract(client,txs,url)
                        if result2 is None:
                            logger.warning("received None from Nodes,may receipt not available the moment")
                            continue 
                        
                        contract=result2
                        symbol= await get_symbol(client,url,contract)
                        logger.info(f"The symbol is {symbol}")

                last_seen=code

              
                write_last_seen(i)

            await asyncio.sleep(time)



    except Exception as e:
        logger.error(f"Response from Rpc is broken: {e}")
