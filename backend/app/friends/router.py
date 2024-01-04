import jwt

from fastapi import APIRouter, Depends
from fastapi import Cookie, Response
from fastapi import HTTPException
from passlib.context import CryptContext
from mongoengine import NotUniqueError
from bson.objectid import ObjectId

from ..auth.main import verify_token, get_user
from ..auth.models import User
from .db import add_friend_request, delete_friend_request

router = APIRouter(
    prefix='/friend',
    tags=['Friend']
)

@router.post('/friend')
async def friend(
        user_id: str,
        current_user: dict = Depends(verify_token)):
    
    friend_to = get_user(user_id)
    friend_from = get_user(current_user['user_id'])

    if friend_to is None:
        raise HTTPException(status_code=400, detail='incorrect user_id')
    
    if ObjectId(current_user['user_id']) in [i.id for i in friend_to.friends]:
        raise HTTPException(status_code=400, detail='already friends')

    add_friend_request(current_user['user_id'], user_id)

    return {'status': '200'}


@router.delete('/friend')
async def friend(
        user_id: str,
        current_user: dict = Depends(verify_token)):
    
    friend_to = get_user(user_id)
    friend_from = get_user(current_user['user_id'])

    if friend_to is None:
        raise HTTPException(status_code=400, detail='incorrect user_id')
    
    if ObjectId(current_user['user_id']) not in [i.id for i in friend_to.friends]:
        raise HTTPException(status_code=400, detail='already not friends')

    delete_friend_request(current_user['user_id'], user_id)

    return {'status': '200'}



    
    