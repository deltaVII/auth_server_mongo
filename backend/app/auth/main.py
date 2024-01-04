from fastapi import Depends, Header
from fastapi import HTTPException
from fastapi import Cookie, Response


from .jwt import verify_access_token
from .models import User
from .db import get_user_as_email


'''
Функции для использования в зависимостях
'''

async def verify_token(
        Authorization: str|None = Header()) -> dict:

    decoded_data = verify_access_token(Authorization.split()[1])
    if decoded_data is None:
        raise HTTPException(
            status_code=400, detail='Invalid token')
    return decoded_data

async def get_user(
        token_data: dict = Depends(verify_token)) -> dict:

    user = get_user_as_email(token_data['email'])
    return dict(user)

def get_session(
        session: str | None = Cookie(default=None)) -> str: 
    if session is None:
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    return session
