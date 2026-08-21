import httpx
import asyncio


payload={
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":["0x3669df8",True],
    "id":1
}

payload2={
    "jsonrpc":"2.0",
    "method":"eth_getTransactionReceipt",
    "params":["0x90f14aa3e248872f0bbf8c5e0f3e57085c4a720a7177a3115c2ea05b936f70b0"],
    "id":1
}

async def get_block():
    async with httpx.AsyncClient() as client:
        r=await client.post("https://rpc.testnet.arc.io",json=payload,timeout=20.0)
        r.raise_for_status()

        rt=await client.post("https://rpc.testnet.arc.io",json=payload2,timeout=20.0)
        rt.raise_for_status()
        
        result=r.json()["result"]["transactions"]

        result2=rt.json()["result"] ["contractAddress"]

        for tx in result:
            if tx["to"] is None:
                print(f"Copntract is created by{tx["from"]}")

        for tx in result2:
            print(tx,end="")

            
        
asyncio.run(get_block())