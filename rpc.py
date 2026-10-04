import logging

logger = logging.getLogger(__name__)
RPC_FAILURE = object()


async def get_current_block(client, url):
    payload3 = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
    try:
        rt = await client.post(url, json=payload3, timeout=20.0)
        rt.raise_for_status()
        result = rt.json()["result"]

        return result

    except Exception:
        logger.exception("Failed to fetch chain head")
        return None


def decode_symbol(result):
    cl = result[2:]
    syms = cl[64:128]
    sym = int(syms, 16)
    symm = bytes.fromhex(cl[128 : 128 + sym * 2]).decode()
    return symm


async def get_symbol(client, url, contract):
    payload3 = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": contract, "data": "0x95d89b41"}, "latest"],
        "id": 1,
    }
    try:
        rt = await client.post(url, json=payload3, timeout=20.0)
        rt.raise_for_status()
        data = rt.json()
        if "error" in data:
            if data["error"]["code"] == 3:
                return None
            else:
                logger.warning(
                    f"couldn't able to fetch the symbol for the contract:{contract} the reason is{data['error']} "
                )
                return RPC_FAILURE

        else:
            result = data["result"]
            if result == "0x":
                return None
        try:
            sym = decode_symbol(result)
            return sym

        except Exception:  # noqa: BLE001
            logger.warning(
                f"Failed to decode the string:{result} ,for the contract:{contract}"
            )
            return None

    except Exception:
        logger.exception(
            f"Failed to call or get response from rpc for the contract:{contract}"
        )
        return RPC_FAILURE


async def get_chain_id(client, url):
    payload = {"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1}
    try:
        rt = await client.post(url, json=payload, timeout=20)
        rt.raise_for_status()
        result = rt.json()["result"]
        chainId = int(result, 16)
        return chainId

    except Exception:
        logger.exception("Failed to fetch chain id")
        return None


async def get_block_receipts(client, number, url):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockReceipts",
        "params": [number],
        "id": 1,
    }

    try:
        rt = await client.post(url, json=payload, timeout=20.0)
        rt.raise_for_status()
        data = rt.json()

        if "error" in data:
            logger.warning(
                f"endpoint returns error for the block:{number} , the reason is {data['error']}"
            )
            return None

        receipt = data["result"]

        if receipt is None:
            logger.warning(f"Node doesn't have the block:{number}")

            return None

        return receipt

    except Exception:
        logger.exception(f"Failed to fetch block:{number}")
        return None
