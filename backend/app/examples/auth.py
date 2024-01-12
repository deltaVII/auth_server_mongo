from fastapi import APIRouter, Depends
from pymongo.database import Database

from ..database import get_database
from ..auth.dependencies import verify_token
from ..auth.main import get_user


router = APIRouter(
    prefix='/test_auth',
    tags=['Test']
)

@router.get('/verify')
async def get_user_me(
        current_user: dict = Depends(verify_token)):

    return current_user
