import httpx
import asyncio

from rpc import gets_block


async def get_block():
    async with httpx.AsyncClient() as client:
        result=await gets_block(client,"0x3669df8")

        for tx in result:
                    if tx["to"] is None:
                           payload2={
                                "jsonrpc":"2.0",
                                "method":"eth_getTransactionReceipt",
                                "params":[tx["hash"]],
                                "id":1
                            }
                           rt=await client.post("https://rpc.testnet.arc.io",json=payload2,timeout=20.0)
                           rt.raise_for_status()
                           result2=rt.json()["result"] ["contractAddress"]
                           print(f"Contract Address is {result2}")

                         

if __name__=="__main__":                        
  asyncio.run(get_block())

                    
                                                
                        
                    

        
        
        

       

        