from peewee import CharField

from database.models.base import BaseModel


class Photos(BaseModel):
    file_name = CharField()
