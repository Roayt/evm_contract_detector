from rpc import get_latest_arc_block,gets_block,get_contract
import asyncio

async def get_latest_block(client):
    while True:
     num=await get_latest_arc_block(client)
     

     result= await gets_block(client,num)
     for txs in result:
        if txs["to"] is  None:
            result2= await get_contract(client,txs)
            print(f"Contract Address is {result2}")
     await asyncio.sleep(2)
    

    
    

