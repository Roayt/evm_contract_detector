import os

from dotenv import load_dotenv

load_dotenv()


def load_data():
    token = os.getenv("Telegram_Token")

    chatId = os.getenv("Telegram_Chat_Id")

    dsn = os.getenv("DATABASE_URL")

    if not token:
        raise ValueError(
            "token opbject returned None object None object, telegram alert cannot be delivered"
        )

    if not chatId:
        raise ValueError(
            "received None object from chatId,  telegram alert cannot br delivered"
        )

    if not dsn:
        raise ValueError("received None object from dsn")

    telegram_Rpc = f"https://api.telegram.org/bot{token}/sendMessage"

    return chatId, telegram_Rpc, dsn
