import httpx
import asyncio
from blocks import get_latest_block
from config import load_data
from db import pool
from rpc import get_chain_id

import argparse

import logging
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(asctime)s - %(name)s -%(message)s',
                    filename='evm_contract_detector.log',
                    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)                                   
async def get_block():

    parser=argparse.ArgumentParser()
    parser.add_argument("--rpc-url",required=True)
    parser.add_argument("--interval",type=int,default=2)
    parser.add_argument("--start-block",type=int,default=None )
    parser.add_argument("--symbol",required=True)
    parser.add_argument("--address",action="append")
    args=parser.parse_args()

    if args.address:
       args.address=[adii.lower() for adii in args.address]
    logger.info(f"RPC_URL:{args.rpc_url}")

    logger.warning("Token tickers on a blockchain are not unique. Anyone can create a token with any ticker and deploy it. \n" \
    "The thing that is unique is contract address, as every token deployed on a blockchain has a different contract address.")

    chatId,rpc,dsn=load_data()

    db_pool=await pool(dsn)
    try:
        async with httpx.AsyncClient() as client: 
              chain_number= await get_chain_id(client,args.rpc_url)
              if chain_number is None:
                    raise ValueError("Received None from get_chain_id function")
            
              await get_latest_block(client,args.rpc_url,args.interval,
                                    args.start_block,args.symbol,args.address,chatId,rpc,chain_number,db_pool)
    finally: 
           await db_pool.close()
 
        
if __name__=="__main__":                         
  asyncio.run(get_block())                        
