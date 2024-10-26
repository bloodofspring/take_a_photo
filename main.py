import os
from colorama import Fore, init
from datetime import datetime

from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message, CallbackQuery

from bot_instance import client

from config import OWNER_ID


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

        file_name = (
            f"@mazutta_photos/Photo("
            f"date={now.day}/{now.month}/{now.year}/t/{now.hour}/{now.minute}/{now.second}"
            f")"
        )
        await request.download(file_name=file_name)
        await request.reply_text(text="Сохранение произведено успешно!")

        await self.stop_client()

    @staticmethod
    async def stop_client():
        print((
                Fore.LIGHTYELLOW_EX + "[!] " +
                Fore.LIGHTWHITE_EX + "Клиент отправлен в режим сна. Следующее пробуждение: {}"
        ))
        await client.stop()


def send_notification_to_mazutta():
    client.send_message(chat_id=OWNER_ID, text="Take a photo!")


def add_handlers() -> None:
    for handler in [GetPhoto]:
        client.add_handler(handler().de_pyrogram_handler)
    print("Все обработчики успешно добавлены!")


def run_bot() -> None:
    add_handlers()
    init(autoreset=True)
    try:
        client.run()
        send_notification_to_mazutta()
    except Exception as e:
        print(f"Невозможно запустить клиента! {e}")


if __name__ == "__main__":
    run_bot()
