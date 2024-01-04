from fastapi import APIRouter, Depends
from fastapi import HTTPException

from ..auth.main import get_user, verify_token


router = APIRouter(
    prefix='/test_auth',
    tags=['Test']
)

@router.get('/me')
async def get_user_me(
        current_user: dict = Depends(get_user)):

    return current_user

@router.get('/verify')
async def get_user_me(
        current_user: dict = Depends(verify_token)):

    return current_user
