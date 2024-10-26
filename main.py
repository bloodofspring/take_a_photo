from pyrogram import filters, Client
from pyrogram.filters import photo
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message, CallbackQuery

from database.create import create_tables
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
        await client.save_file(path="test", file_id=int(request.photo.file_id))

    @staticmethod
    def stop_client():
        client.stop()


def send_notification_to_mazutta():
    client.send_message(chat_id=OWNER_ID, text="Take a photo!")


def add_handlers() -> None:
    for handler in [GetPhoto]:
        client.add_handler(handler().de_pyrogram_handler)
    print("Все обработчики успешно добавлены!")


def run_bot() -> None:
    add_handlers()
    create_tables()
    send_notification_to_mazutta()
    try:
        client.run()
    except Exception as e:
        print(f"Невозможно запустить клиента! {e}")


if __name__ == "__main__":
    run_bot()
