import httpx
import asyncio
from blocks import get_latest_block


async def get_block():
    async with httpx.AsyncClient() as client:
        await get_latest_block(client)
        
        

if __name__=="__main__":                         
  asyncio.run(get_block())                        


                    
                                                
                        
                    

        
        
        

       

        