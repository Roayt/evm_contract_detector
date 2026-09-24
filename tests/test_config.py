import pytest

from config import load_data


def test_loadata(monkeypatch):
    monkeypatch.setenv("Telegram_Token","testfake2323")
    monkeypatch.setenv("Telegram_Chat_Id","8686987")
    monkeypatch.setenv("DATABASE_URL","irhiheirhii")
    chatId,telegram_Rpc,dsn=load_data()

    assert chatId=="8686987"
    assert telegram_Rpc=="https://api.telegram.org/bottestfake2323/sendMessage"
    assert dsn=="irhiheirhii"

def test_value_error_token(monkeypatch):
     monkeypatch.setenv("Telegram_Chat_Id","9834597")
     monkeypatch.delenv("Telegram_Token",raising=False)
     with pytest.raises(ValueError):
        load_data() 

def test_value_error_chatId(monkeypatch):
    monkeypatch.setenv("Telegram_Token","jrjtyopjro945")
    monkeypatch.delenv("Telegram_Chat_Id",raising=False)
    with pytest.raises(ValueError):
        load_data()

def test_value_error_dsn(monkeypatch):
     monkeypatch.setenv("Telegram_Chat_Id","9834597")
     monkeypatch.setenv("Telegram_Token","jrjtyopjro945")
     monkeypatch.delenv("DATABASE_URL",raising=False)
     with pytest.raises(ValueError):
        load_data() 
        