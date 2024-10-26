from typing import Final
from dotenv import load_dotenv
from os import environ

load_dotenv()

OWNER_ID: Final[int] = environ["owner_id"]
