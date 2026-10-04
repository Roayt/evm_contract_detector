import asyncio
import logging

from db import insert_check_point, insert_data
from rpc import (
    RPC_FAILURE,
    get_block_receipts,
    get_current_block,
    get_symbol,
)
from telegram_client import telegram_alert

logger = logging.getLogger(__name__)


async def get_latest_block(
    client,
    url,
    time,
    block_height,
    ticker,
    address,
    chatId,
    rpc,
    chain_number,
    db_pool,
    last_block,
):

    nums = last_block
    if nums is None:
        t = await get_current_block(client, url)
        if t is None:
            raise ValueError("Im receiving none object from latest block")
        last_seen = int(t, 16)
        logger.warning(f"checkpoint not exists for chain:{chain_number}")

    else:
        last_seen = nums

    if block_height:
        logger.info(
            f"The block height:{block_height} ,provided with --start-block overides database checkpoint"
        )
        last_seen = block_height

    logger.info(f"The block processing will start from:{last_seen + 1}")
    while True:
        try:
            num = await get_current_block(client, url)
            code = int(num, 16)
        except Exception as e:  # noqa: BLE001
            logger.warning(f"couldn't fetch the block height,trying again: {e}")
            await asyncio.sleep(time)
            continue

        try:
            for i in range(last_seen + 1, code + 1):
                blocknum = hex(i)
                receipts = await get_block_receipts(client, blocknum, url)
                if receipts is None:
                    logger.error(f"Received None from get_block_receipts: {i}")
                    await asyncio.sleep(time)
                    break
                block_failed = False

                for receipt in receipts:
                    if receipt["to"] is None:
                        if receipt["status"] == "0x0":
                            continue
                        froms = receipt["from"]

                        if address is not None and froms.casefold() not in address:
                            continue

                        contract = receipt["contractAddress"]

                        symbols = await get_symbol(client, url, contract)
                        if symbols is None:
                            logger.debug(
                                f"received None object from symbol call, the contract received None symbol is {contract}"
                            )
                            continue

                        if symbols is RPC_FAILURE:
                            block_failed = True
                            break

                        if symbols.casefold() == ticker.casefold():
                            logger.info(
                                f"From: {froms} , Contract Address: {contract} Symbol: {symbols}"
                            )

                            message = (
                                "Contract detected! 🚨\n"
                                f"Creator:{froms}\n"
                                f"Contract Address:{contract}\n"
                                f"Symbol:{symbols}"
                            )

                            insert_status = await insert_data(
                                db_pool, contract, chain_number, symbols, i, froms
                            )
                            if insert_status is None:
                                block_failed = True
                                break
                            alert_sent = await telegram_alert(
                                client, message, chatId, rpc
                            )
                            if alert_sent is False:
                                block_failed = True
                                break
                        else:
                            logger.debug(
                                f"from:{froms},Contract Address:{contract} Symbol:{symbols}"
                            )

                if block_failed:
                    logger.warning(f"Block:{i} got failed, retrying again....")
                    break
                last_seen = i

                await insert_check_point(db_pool, chain_number, i)
        except Exception:
            logger.exception("Unexpected error while processing the blocks")

        await asyncio.sleep(time)
