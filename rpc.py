async def gets_block(client,number):
    payload={
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":[number,True],
    "id":1
}
    try:
        r=await client.post("https://rpc.testnet.arc.io",json=payload,timeout=20.0)
        r.raise_for_status()
            
        result=r.json()["result"]["transactions"]
        return result
    
    except Exception:
          return None 

async def get_contract(client,tx):
            payload2={
                "jsonrpc":"2.0",
                "method":"eth_getTransactionReceipt",
                "params":[tx["hash"]],
                "id":1
            }

            try:
                rt=await client.post("https://rpc.testnet.arc.io",json=payload2,timeout=20.0)
                rt.raise_for_status()
                result2=rt.json()["result"]["contractAddress"]

                if result2 is None:
                      print("Transaction Receipt deleted from the Node")
                
                return result2

            except Exception:
                   return None

async def get_latest_arc_block(client):
        payload3={
                "jsonrpc":"2.0",
                "method":"eth_blockNumber",
                "params":[],
                "id":1
        }
        try:

            rt=await client.post("https://rpc.testnet.arc.io",json=payload3,timeout=20.0)
            rt.raise_for_status()
            result=rt.json()["result"]

            return result

        except Exception:
            return None 
            

    




    
