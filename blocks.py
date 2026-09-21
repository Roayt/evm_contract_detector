from rpc import get_latest_arc_block,gets_block,get_contract,get_symbol
import asyncio
from telegram_client import telegram_alert
from db import insert_data,insert_check_point
import logging
logger=logging.getLogger(__name__)    

async def get_latest_block(client,url,time,block_height,ticker,address,chatId,rpc,chain_number,db_pool,last_block):

    try:

        nums=last_block
        if nums is None:

            t=await get_latest_arc_block(client,url)
            if t is None:
                raise ValueError("Im receiving none object")
            last_seen=int(t,16)
            logger.warning(f"checkpoint not exists for chain:{chain_number}, starting from current head:{last_seen}") 


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
                    logger.error(f"Received None from get_block, object continuing back the loop: {i}")
                    await asyncio.sleep(time)
                    break                                             
                           
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
                                await insert_data(db_pool,result2,chain_number,symbols,i,froms)
                        else:
                            logger.debug(f"from:{froms},Contract Address:{result2} Symbol:{symbols}") 

                
                last_seen=i

                await insert_check_point(db_pool,chain_number,i)

            await asyncio.sleep(time)


    except Exception as e:
        logger.error(f"Response from Rpc is broken: {e}")
