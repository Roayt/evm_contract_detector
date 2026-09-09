import os 
from dotenv import load_dotenv

load_dotenv()

token=os.getenv("Telegram_Token")

telegram_Rpc=f"https://api.telegram.org/bot{token}/SendMessage"

chatId=os.getenv("Telegram_Chat_Id")

