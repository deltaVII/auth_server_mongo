from fastapi import Depends, Header
from fastapi import HTTPException
from fastapi import Cookie, Response


from .jwt import verify_access_token
from .models import User
from .db import get_user as get_user_db


'''
Функции для использования в зависимостях
'''

def verify_token(
        Authorization: str|None = Header()) -> dict:

    decoded_data = verify_access_token(Authorization.split()[1])
    if decoded_data is None:
        raise HTTPException(
            status_code=400, detail='Invalid token')
    return decoded_data

def get_user(
        user_id: str) -> User:

    return get_user_db(user_id)

def get_session(
        session: str | None = Cookie(default=None)) -> str: 
    if session is None:
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    return session
