import httpx
import asyncio
from blocks import get_latest_block

import argparse

import logging
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(asctime)s - %(name)s -%(message)s',filename='evm_contract_detector.log',
                    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)                                   
async def get_block():

    parser=argparse.ArgumentParser()
    parser.add_argument("--rpc-url",required=True)
    parser.add_argument("--interval",type=int,default=2)
    parser.add_argument("--start-block",type=int,default=None )
    parser.add_argument("--symbol",required=True)
    args=parser.parse_args()
    logger.info(f"RPC_URL:{args.rpc_url}")

    logger.warning("Token tickers on a blockchain are not unique. Anyone can create a token with any ticker and deploy it. \n" \
    "The thing that is unique is contract address, as every token deployed on a blockchain has a different contract address.")
    async with httpx.AsyncClient() as client:
        await get_latest_block(client,args.rpc_url,args.interval,args.start_block,args.symbol)
   
        
if __name__=="__main__":                         
  asyncio.run(get_block())                        




        
          

       

        
