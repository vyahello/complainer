"""Provide API authentication routes."""
from typing import Any, Callable, Coroutine, Dict

from fastapi import APIRouter

from complainer.managers.user import UserManager
from complainer.schemas.request.user import UserLogin, UserRegisterIn

router = APIRouter(tags=['Auth API'])


async def __response(
    method: Callable[[Any], Coroutine[Any, Any, str]], user_data: Any
) -> Dict[str, str]:
    """Return auth request response."""
    return {'token': await method(user_data.dict())}


@router.post('/register', status_code=201)
async def register(user_data: UserRegisterIn) -> Dict[str, str]:
    """Register a user."""
    return await __response(UserManager.register, user_data)


@router.post('/login')
async def login(user_data: UserLogin) -> Dict[str, str]:
    """Login a user."""
    return await __response(UserManager.login, user_data)
