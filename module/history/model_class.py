
from peewee import *


DB = SqliteDatabase('bot_db.db')


class User(Model):
    """
    Класс представляет таблицу Users с информацией о пользователях
    """

    user_id = IntegerField()

    class Meta:
        database = DB
        table_name = 'users'


class Command(Model):
    """
    Класс представляет таблицу Commands с информацией об истории поиска
    """

    cmd_name = CharField()
    created_at = DateTimeField()
    result = TextField()
    user = ForeignKeyField(User, backref='cmds')

    class Meta:
        database = DB
        table_name = 'commands'
