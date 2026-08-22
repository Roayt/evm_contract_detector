import httpx
import asyncio


payload={
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":["0x3669df8",True],
    "id":1
}
async def get_block():
    async with httpx.AsyncClient() as client:
        r=await client.post("https://rpc.testnet.arc.io",json=payload,timeout=20.0)
        r.raise_for_status()

        result=r.json()["result"]["transactions"]

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

asyncio.run(get_block())
                    
                                                
                        
                    

        
        
        

       

        