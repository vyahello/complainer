"""Provide API authentication resources."""
from typing import Dict

from fastapi import APIRouter

from complainer.managers.user import UserManager

router = APIRouter(tags=['Auth'])


@router.post('/register', status_code=201)
async def register(user_data: Dict[str, str]) -> Dict[str, str]:
    """Represents app '/register' endpoint."""
    return {'token': await UserManager.register(user_data)}


@router.post('/login')
async def login(user_data: Dict[str, str]) -> Dict[str, str]:
    """Represents app '/login' endpoint."""
    return {'token': await UserManager.login(user_data)}
