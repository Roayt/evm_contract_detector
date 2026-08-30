import httpx
import asyncio
from blocks import get_latest_block

import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s - %(name)s -%(message)s',filename='arc_monitor.log',
                    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)                                   
async def get_block():
    async with httpx.AsyncClient() as client:
        await get_latest_block(client)
        
        

if __name__=="__main__":                         
  asyncio.run(get_block())                        

        
        

       

        
