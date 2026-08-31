import httpx
import asyncio
from blocks import get_latest_block
from config import ARC_RPC_URL

import argparse

import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s - %(name)s -%(message)s',filename='arc_monitor.log',
                    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)                                   
async def get_block():

    parser=argparse.ArgumentParser()
    parser.add_argument("--rpc-url",default=ARC_RPC_URL)
    parser.add_argument("--interval",type=int,default=2)
    parser.add_argument("--start-block",type=int,default=None )
    args=parser.parse_args()
    print(args.rpc_url)
    async with httpx.AsyncClient() as client:
        await get_latest_block(client,args.rpc_url,args.interval,args.start_block)
   
        
if __name__=="__main__":                         
  asyncio.run(get_block())                        




        
          

       

        
