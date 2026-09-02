import logging
logger=logging.getLogger(__name__)

async def gets_block(client,number,url):
    payload={
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":[number,True],
    "id":1
}
    try:
        r=await client.post(url,json=payload,timeout=20.0)
        r.raise_for_status()
            
        result=r.json()["result"]["transactions"]
        return result
    
    except Exception:
          return None 

async def get_contract(client,tx,url):
            payload2={
                "jsonrpc":"2.0",
                "method":"eth_getTransactionReceipt",
                "params":[tx["hash"]],
                "id":1
            }

            try:
                rt=await client.post(url,json=payload2,timeout=20.0)
                rt.raise_for_status()
                result2=rt.json()["result"]["contractAddress"]

                if result2 is None:
                      logger.warning("Transaction Receipt deleted from the Node")
                
                return result2

            except Exception:
                   return None

async def get_latest_arc_block(client,url):
        payload3={
                "jsonrpc":"2.0",
                "method":"eth_blockNumber",
                "params":[],
                "id":1
        }
        try:

            rt=await client.post(url,json=payload3,timeout=20.0)
            rt.raise_for_status()
            result=rt.json()["result"]

            return result

        except Exception:
            return None 

async def get_symbol(client,url,contract):
        payload3={
                "jsonrpc":"2.0",
                "method":"eth_call",
                "params":[{"to":contract,"data":"0x95d89b41"},"latest"],
                "id":1
        }
        try:

            rt=await client.post(url,json=payload3,timeout=20.0)
            rt.raise_for_status()
            data=rt.json()
            if "error"  in data:
                  return None 
            else:
            
                result=data ["result"]
                if result=="0x":
                      return None

                cl=result[2:]
                syms=cl[64:128]
                sym=int(syms,16)
                symm=bytes.fromhex(sym).decode()
                return symm
        except Exception as e:
            return f"received non object from symbol call{e}"
            

    




    
