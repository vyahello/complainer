"""Provide API user routes."""
from typing import List, Optional, Union

from databases.backends.postgres import Record
from fastapi import APIRouter, Depends

from complainer.managers.auth import is_admin, oauth2_scheme
from complainer.managers.user import UserManager

router = APIRouter(tags=['Users API'])


@router.get('/users', dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def get_users(email: Optional[str] = None) -> Union[Record, List[Record]]:
    """Fetch all users."""
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()
