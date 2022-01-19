"""Provide API authentication resources."""
from typing import Dict

from fastapi import APIRouter

from complainer.managers.user import UserManager
from complainer.schemas.request.user import UserLogin, UserRegisterIn

router = APIRouter(tags=['Auth'])


@router.post('/register', status_code=201)
async def register(user_data: UserRegisterIn) -> Dict[str, str]:
    """Represents app '/register' endpoint."""
    return {'token': await UserManager.register(user_data.dict())}


@router.post('/login')
async def login(user_data: UserLogin) -> Dict[str, str]:
    """Represents app '/login' endpoint."""
    return {'token': await UserManager.login(user_data.dict())}
