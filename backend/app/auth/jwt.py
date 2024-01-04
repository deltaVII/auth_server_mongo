import jwt
from datetime import datetime
from datetime import timedelta

from config import SECRET_KEY
from .models import User

ALGORITHM = 'HS256'
EXPIRATION_TIME = {
    'access_token': timedelta(minutes=30), 
    'refresh_token': timedelta(days=30),
}


def verify_access_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError as ex:
        return None
    
def verify_refresh_token(token: str):
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_data
    

def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME[data['type']]
    data.update({'exp': expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_tokens(user: User) -> list[dict]:
    new_refresh_token = create_jwt_token({
        'user_id': user['id'].__str__(),
        'username': user['username'],                   
        'email': user['email'],
        'type': 'refresh_token',
    })
    new_access_token = create_jwt_token({
        'user_id': user['id'].__str__(),
        'username': user['username'],                   
        'email': user['email'],
        'type': 'access_token',
    })
    return new_refresh_token, new_access_token
