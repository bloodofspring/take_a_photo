from typing import Final

from peewee import SqliteDatabase

db: Final[SqliteDatabase] = SqliteDatabase("filenames_archive")
