from fastapi import HTTPException
from bson.objectid import ObjectId
from mongoengine import NotUniqueError

from .models import User, UserSession


def create_user(
        username: str,
        email: str,
        hashed_password: str):
    
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    try:
        new_user.save()
    except NotUniqueError:
        raise HTTPException(
            status_code=409, detail='Email or username already registered')
    
def get_user_as_email(
        email: str):
    
    user = User.objects(email=email).first()

    if user is None: # нужны ли они здесь?
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')
    return user
    

def get_user_session(
        token: str):
    
    user_session = UserSession.objects(token=token).first()
    if user_session is None: 
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    return user_session

def create_user_session(
        token: str,
        user_id: str):
    
    session = UserSession(
        token=token,
        user_id=ObjectId(user_id)
    )
    session.save()

def update_user_session(
        new_token: str,
        old_token: str):
    
    UserSession.objects(token=old_token).update(token=new_token)

def delete_user_session(
        token: str):
    
    user_session = UserSession.objects(token=token).delete()
    if user_session == 0:
        raise HTTPException(
            status_code=400, detail='Incorrect token')

