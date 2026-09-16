from rpc import get_latest_arc_block,gets_block,get_contract,get_symbol
import asyncio
from last_seen import write_last_seen,read_last_seen
from telegram_client import telegram_alert
import logging
logger=logging.getLogger(__name__)    

async def get_latest_block(client,url,time,block_height,ticker,address,chatId,rpc):

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
                    logger.error("Received None from get_block, object continuine back the loop")
                    await asyncio.sleep(time)
                    continue                                                
                           
                for txs in result:
                    if txs["to"] is  None:
                        froms=txs["from"]

                        if address is not None and froms.casefold() not in address:
                             continue
                        
                        result2= await get_contract(client,txs,url)
                
                        if result2 is None:
                            logger.warning("received None from get_contract,may receipt not available at the moment")
                            continue 
                        
                        contract=result2
                        symbols= await get_symbol(client,url,contract)
                        if symbols is None:
                             logger.debug(f"received None object from symbol call, the contract received None symbol is {contract}")
                             continue

                
                        if symbols.casefold() ==ticker.casefold():
                                logger.info(f"From: {froms} , Contract Address: {result2} Symbol:{symbols}")

                                message=("Contract detected! 🚨\n"
                                                f"Creatore:{froms}\n"
                                                f"Contract Address:{result2}\n"
                                                f"Symbol:{symbols}")
                                
                                await telegram_alert(client,message,chatId,rpc)
                        else:
                            logger.debug(f"from:{froms},Contract Address:{result2} Symbol:{symbols}") 

                        

                
                last_seen=i
              
                write_last_seen(i)

            await asyncio.sleep(time)


    except Exception as e:
        logger.error(f"Response from Rpc is broken: {e}")
