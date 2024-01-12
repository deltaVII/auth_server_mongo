import jwt

from fastapi import APIRouter, Depends
from fastapi import Cookie, Response
from fastapi import HTTPException
from passlib.context import CryptContext
from bson.objectid import ObjectId
from pymongo.database import Database

from .jwt import create_tokens, verify_refresh_token
from .schemas import CreateUser, LoginUser
from .dependencies import get_session
from .repository import UserRepository, UserSessionRepository
from .utils import is_user_already_registered, verify_user_session
from ..database import get_database

'''
Необходимые эндпоинты для авторизации

Если это возможно то обработка исключений происходит в db.py
'''

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/register',
    responses={
        200: {'status': '200'},
        409: {
            'example 1': {'detail': 'email already registered'},
            'example 2': {'detail': 'username already registered'}}})
async def register_user(
        new_user: CreateUser,
        database: Database= Depends(get_database)):
    
    user_repository = UserRepository(database)

    # она еще вызывает аштитипи ексепты
    is_user_already_registered(new_user.username, 
                               new_user.email,
                               user_repository)
    
    hashed_password = pwd_context.hash(new_user.password)
    user_repository.add_one({
        'username': new_user.username,
        'email': new_user.email,
        'hashed_password': hashed_password
    })

    return {'status': '200'}


@router.post('/login',
    responses={
        200: {
            'session': {
                'token': 'refresh_token',
                'type': 'cookie'}, 
            'access_token': {
                'token': 'access_token',
                'type': 'bearer'}},
        400: {'detail': 'Incorrect username or password'}})
async def login_user(
        response: Response,
        login_user: LoginUser,
        database: Database= Depends(get_database)):

    user_repository = UserRepository(database)
    user_session_repository = UserSessionRepository(database)
    
    user = user_repository.find_one({'email': login_user.email}) # ошибку

    is_password_correct = pwd_context.verify(
        login_user.password, 
        user['hashed_password'])
    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')
    
    refresh_token, access_token = create_tokens(user)
    user_session_repository.insert_one(user['id'], refresh_token)

    response.set_cookie(key='session', value=refresh_token, 
                        httponly=True, max_age=60*60*24*30)
    return {
        'session': {
            'token': refresh_token,
            'type': 'cookie'}, 
        'access_token': {
            'token': access_token,
            'type': 'bearer'}}


@router.put('/token',
    responses={
        200: {
            'session': {
                'token': 'refresh_token',
                'type': 'cookie'}, 
            'access_token': {
                'token': 'access_token',
                'type': 'bearer'}},
        400: {'detail': 'Incorrect token'}})
async def update_session(
        response: Response,
        session: str | None = Depends(get_session),
        database: Database= Depends(get_database)):

    user_session_repository = UserSessionRepository(database)
    
    # она еще вызывает аштитипи ексепты
    token_data = verify_user_session(session, user_session_repository)

    # так как в токене поле "user_id" а не "id"
    token_data['id'] = token_data['user_id'] 

    refresh_token, access_token = create_tokens(token_data)
    is_update = user_session_repository.update_one(session, refresh_token)
    if is_update == 0:
        raise HTTPException(
            status_code=400, detail='Incorrect token')

    response.set_cookie(key='session', value=refresh_token, 
                        httponly=True, max_age=60*60*24*30)
    return {
        'session': {
            'token': refresh_token,
            'type': 'cookie'}, 
        'access_token': {
            'token': access_token,
            'type': 'bearer'}}


@router.delete('/token',
    responses={
        200: {'status': '200'},
        400: {'detail': 'Incorrect token'}})
async def logout(
        response: Response,
        session: str | None = Depends(get_session),
        database: Database= Depends(get_database)):

    user_session_repository = UserSessionRepository(database)

    token_data = verify_user_session(session, user_session_repository)
    
    user_session_repository.delete_one(session)
    response.delete_cookie(key='session')

    return {'status': '200'}

