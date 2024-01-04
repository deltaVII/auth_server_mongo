from fastapi import FastAPI
from mongoengine import connect 

from .auth.router import router as auth_router
from .friends.router import router as friends_router
from .examples.auth import router as test_auth_router
from config import DB_URL

app = FastAPI()

connect(host=DB_URL)

@app.get('/')
def root():
    return {'message': 'Hello world'}


app.include_router(
    auth_router
)
app.include_router(
    friends_router
)
app.include_router(
    test_auth_router
)


