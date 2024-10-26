from os import environ
from typing import Final

from dotenv import load_dotenv

load_dotenv()

OWNER_ID: Final[int] = int(environ["owner_id"])
