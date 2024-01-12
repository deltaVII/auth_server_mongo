from datetime import datetime

from bson.objectid import ObjectId
from pydantic import BaseModel



class UserSession(BaseModel):
    token: str

    created_at: datetime = datetime.utcnow
    updated_at: datetime = datetime.utcnow


class User(BaseModel):
    id: str
    email: str
    username: str
    hashed_password: str

    #friends: list
    #sessions: list

    created_at: datetime = datetime.utcnow
    updated_at: datetime = datetime.utcnow
