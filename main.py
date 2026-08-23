import httpx
import asyncio

from rpc import gets_block,get_contract


async def get_block():
    async with httpx.AsyncClient() as client:
        result= await gets_block(client,"0x3669df8")
        for txs in result:
           if txs["to"] is  None:
            result2= await get_contract(client,txs)
            print(f"Contract Address is {result2}")

if __name__=="__main__":                        
  asyncio.run(get_block())                        


                    
                                                
                        
                    

        
        
        

       

        