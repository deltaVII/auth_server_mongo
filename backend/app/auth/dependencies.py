from fastapi import Header
from fastapi import HTTPException
from fastapi import Cookie

from .jwt import verify_access_token


def verify_token(
        Authorization: str|None = Header()) -> dict:

    decoded_data = verify_access_token(Authorization.split()[1])
    if decoded_data is None:
        raise HTTPException(
            status_code=400, detail='Invalid token')
    decoded_data['id'] = decoded_data['user_id']
    return decoded_data


def get_session(
        session: str | None = Cookie(default=None)) -> str: 
    if session is None:
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    return session