from fastapi import APIRouter, Depends
from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database

from ..auth.dependencies import verify_token
from ..auth.utils import UserRepository
from ..database import get_database
from .repository import FriendRepository


router = APIRouter(
    prefix='/friend',
    tags=['Friend']
)

@router.post('/friend')
async def friend(
        user_id: str,
        current_user: dict = Depends(verify_token),
        database: Database= Depends(get_database)):
    
    friend_repository = FriendRepository(database)
    user_repository = UserRepository(database)
    
    friend_to = user_repository.get_by_id(user_id)
    friend_from = user_repository.get_by_id(current_user['user_id'])

    if friend_to is None:
        raise HTTPException(status_code=400, detail='incorrect user_id')
    
    if ObjectId(user_id) in [i for i in friend_from.get('friends')]:
        raise HTTPException(status_code=400, detail='already friends')

    friend_repository.add(user_id, current_user['user_id'])

    return {'status': '200'}


@router.delete('/friend')
async def friend(
        user_id: str,
        current_user: dict = Depends(verify_token),
        database: Database= Depends(get_database)):
    
    friend_repository = FriendRepository(database)
    user_repository = UserRepository(database)
    
    friend_to = user_repository.get_by_id(user_id)
    friend_from = user_repository.get_by_id(current_user['user_id'])

    if friend_to is None:
        raise HTTPException(status_code=400, detail='incorrect user_id')
    
    if ObjectId(user_id) not in [i for i in friend_from.get('friends')]:
        raise HTTPException(status_code=400, detail='already not friends')

    friend_repository.delete(user_id, current_user['user_id'])

    return {'status': '200'}



    
    