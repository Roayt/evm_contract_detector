from rpc import get_latest_arc_block,gets_block,get_contract
import time 
import asyncio


async def get_latest_block(client):

    try:
        nums=await get_latest_arc_block(client)
        if nums is None:
            raise ValueError("Rpc returned None object")
        
        last_seen=(int(nums,16))

        while True:
             

            num=await get_latest_arc_block(client)
            code=int(num,16)
            for i in range(last_seen +1,code+1):
                blocknum=(hex(i))
        
        
            result= await gets_block(client,blocknum)

            if result is None:
                    print("Received None object continuinf back the loop")
                    await asyncio.sleep(5)
                    continue
            
            for txs in result:
                if txs["to"] is  None:
                    result2= await get_contract(client,txs)
                    if result2 is None:
                        print("received None from Nodes,may receiptnot available the moment")
                        continue 
                    
                    print(f"Contract Address is {result2}")
            last_seen=code
            await asyncio.sleep(2)

    except Exception as e:
        print(f"Response from Rpc is broken: {e}")
