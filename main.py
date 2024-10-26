import os
from datetime import datetime, timedelta
from random import randint

from colorama import Fore, init
from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message, CallbackQuery

from bot_instance import pyrogram_client, telebot_client
from config import OWNER_ID
from database.create import create_tables
from database.models import Photos


class BaseHandler:
    """Базовый обработчик-исполнитель"""
    __name__ = ""
    HANDLER: Handler = MessageHandler
    FILTER: filters.Filter | None = None

    def __init__(self):
        self.client: Client | None = None
        self.request: Message | CallbackQuery | None = None

    async def func(self, client_: Client, request: Message | CallbackQuery):
        raise NotImplementedError

    @property
    def de_pyrogram_handler(self):
        return self.HANDLER(self.func, self.FILTER)


class GetPhoto(BaseHandler):
    FILTER = filters.photo

    async def func(self, _, request: Message):
        now = datetime.now()

        if not os.path.exists("@mazutta_photos"):
            os.mkdir("@mazutta_photos")

        file_name = (f"@mazutta_photos/Photo("
                     f"date={now.day}_{now.month}_{now.year},"
                     f"time={now.hour}_{now.minute}_{now.second}"
                     f")")
        await request.download(file_name=file_name)
        Photos.create(file_name=file_name)
        await request.reply_text(text="Сохранение произведено успешно!")

        self.stop_client()

    @staticmethod
    def stop_client():
        exit(Fore.LIGHTWHITE_EX + f"[!] Клиент отправлен в режим сна. Следующее пробуждение: {create_new_time_point()}")


def create_new_time_point():
    # 1724 = 28 HRS 44 MINS
    now = datetime.now()
    until_4_44 = 1724 - (now.minute + now.hour * 60)
    send_time = now + timedelta(minutes=randint(until_4_44, until_4_44 + 1440))

    return send_time


def send_notification_to_mazutta() -> None:
    telebot_client.send_message(chat_id=OWNER_ID, text="Take a photo!")


def add_handlers() -> None:
    for handler in [GetPhoto]:
        pyrogram_client.add_handler(handler().de_pyrogram_handler)
    print("Все обработчики успешно добавлены!")


def run_bot() -> None:
    add_handlers()
    create_tables()
    init(autoreset=True)
    send_notification_to_mazutta()
    try:
        pyrogram_client.run()
    except Exception as e:
        print(f"Невозможно запустить клиента! {e}")


if __name__ == "__main__":
    run_bot()
