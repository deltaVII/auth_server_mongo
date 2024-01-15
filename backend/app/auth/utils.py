from fastapi import HTTPException
import jwt

from .repository import UserRepository
from .jwt import verify_refresh_token
from .repository import UserRepository, UserSessionRepository


def is_user_already_registered(
        username: str, 
        email: str, 
        user_repository: UserRepository):
    
    user1 = user_repository.find_one({'email': email})                    
    user2 = user_repository.find_one({'username': username})
    if user1 is not None:
        raise HTTPException(
            status_code=409, detail='email already registered')
    if user2 is not None:
        raise HTTPException(
            status_code=409, detail='username already registered')
    
def verify_user_session(
        token: str, 
        user_session_repository: UserSessionRepository):
    
    try:
        return verify_refresh_token(token)
    except jwt.ExpiredSignatureError:
        user_session_repository.delete_one(token)
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=400, detail='Incorrect token')