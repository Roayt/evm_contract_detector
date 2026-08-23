async def gets_block(client,number):
    payload={
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":[number,True],
    "id":1
}
    r=await client.post("https://rpc.testnet.arc.io",json=payload,timeout=20.0)
    r.raise_for_status()
        
    result=r.json()["result"]["transactions"]

    return result



    




    
