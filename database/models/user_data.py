from peewee import IntegerField, CharField, ForeignKeyField

from database.models.base import BaseModel


class Users(BaseModel):
    tg_id = IntegerField()
    cust_name = CharField()


class UserPhotos(BaseModel):
    file_name = CharField()

    user = ForeignKeyField(Users, backref="photos")
