import jwt

from fastapi import APIRouter, Depends
from fastapi import Cookie, Response
from fastapi import HTTPException
from passlib.context import CryptContext
from mongoengine import NotUniqueError
from bson.objectid import ObjectId

from .jwt import create_tokens, verify_refresh_token
from .schemas import CreateUser, LoginUser
from .db import create_user, get_user_as_email
from .db import get_user_session, create_user_session
from .db import update_user_session, delete_user_session
from .main import get_session

'''
Необходимые эндпоинты для авторизации

Если это возможно то обработка исключений происходит в db.py
'''

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/register')
async def register_user(
        new_user: CreateUser):
    
    hashed_password = pwd_context.hash(new_user.password)

    create_user(new_user.username, new_user.email, hashed_password)

    return {'status': '200'}


@router.post('/login')
async def login_user(
        response: Response,
        login_user: LoginUser):
    
    user = get_user_as_email(login_user.email)

    is_password_correct = pwd_context.verify(
        login_user.password, 
        user.hashed_password)
    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')
    
    refresh_token, access_token = create_tokens(user)
    create_user_session(refresh_token, user.id)

    response.set_cookie(key='session', value=refresh_token, 
                        httponly=True, max_age=60*60*24*30)
    return {
        'session': {
            'token': refresh_token,
            'type': 'cookie'}, 
        'access_token': {
            'token': access_token,
            'type': 'bearer'}
    }


@router.put('/token')
async def update_session(
        response: Response,
        session: str | None = Depends(get_session)):
    
    try:
        token_data = verify_refresh_token(session)
    except jwt.ExpiredSignatureError:
        delete_user_session(session)
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=400, detail='Incorrect token')
    
    _user_session = get_user_session(session)

    token_data['id'] = token_data['user_id'] 
    # так как в токене поле "user_id" а не "id"

    refresh_token, access_token = create_tokens(token_data)
    update_user_session(refresh_token, session)

    response.set_cookie(key='session', value=refresh_token, 
                        httponly=True, max_age=60*60*24*30)
    return {
        'session': {
            'token': refresh_token,
            'type': 'cookie'}, 
        'access_token': {
            'token': access_token,
            'type': 'bearer'}
    }


@router.delete('/token')
async def logout(
        response: Response,
        session: str | None = Depends(get_session)):
    
    delete_user_session(session)
    response.delete_cookie(key='session')

    return {'status': '200'}

