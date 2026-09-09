from config import telegram_Rpc,chatId

import logging
logger=logging.getLogger(__name__)

async def telegram_alert(client,message):

    try:

        payload={
        "chat_id":chatId,
        "text":message,
    }
        await client.post(telegram_Rpc,json=payload)
    except Exception as e:
        logger.error(e)
