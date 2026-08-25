from rpc import get_latest_arc_block,gets_block,get_contract
import time 
import asyncio


async def get_latest_block(client):
    nums=await get_latest_arc_block(client)
    last_seen=(int(nums,16))
    while True:
     num=await get_latest_arc_block(client)
     code=int(num,16)
     for i in range(last_seen,code+1):
        print(i)
     

     result= await gets_block(client,num)
     for txs in result:
        if txs["to"] is  None:
            result2= await get_contract(client,txs)
            print(f"Contract Address is {result2}")
     last_seen=code

     await asyncio.sleep(2)
     




    

    
    

