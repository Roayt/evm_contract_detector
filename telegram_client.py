import logging
logger=logging.getLogger(__name__)

async def telegram_alert(client,message,chatId,telegram_Rpc):

    try:

        payload={
        "chat_id":chatId,
        "text":message,
    }
        t=await client.post(telegram_Rpc,json=payload)
        data=t.json()
        if data["ok"]:
            logger.debug("telegram received the response")
        else:
            logger.error(data["description"])

    except Exception as e:
        logger.error(e)
