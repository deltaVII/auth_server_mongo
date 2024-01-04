from fastapi import HTTPException
from bson.objectid import ObjectId
from mongoengine import NotUniqueError

from ..auth.models import User

def add_friend_request(
        user_to_id: ObjectId,
        user_from_id: ObjectId):
    
    User.objects(id=user_from_id).update(push__friends=user_to_id)


def delete_friend_request(
        user_to_id: ObjectId,
        user_from_id: ObjectId):
    
    User.objects(id=user_from_id).update(pull__friends=user_to_id)