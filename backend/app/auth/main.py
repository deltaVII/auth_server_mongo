from fastapi import Depends
from pymongo.database import Database

from .repository import UserRepository

'''
Функции для использования в зависимостях
'''

def get_user(
        user_id: str,
        database: Database):

    user_repository = UserRepository(database)

    return user_repository.get_by_id(user_id)


