"""Provide API user routes."""
from typing import List, Optional, Union

from databases.backends.postgres import Record
from fastapi import APIRouter, Depends

from complainer.managers.auth import is_admin, oauth2_scheme
from complainer.managers.user import UserManager
from complainer.models import RoleType
from complainer.schemas.response.user import UserOut

router = APIRouter(tags=['Users API'])


@router.get(
    '/users',
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=List[UserOut],
)
async def get_users(email: Optional[str] = None) -> Union[Record, List[Record]]:
    """Fetch all users."""
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put(
    '/users/{user_id}/make-admin',
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int) -> None:
    """Change user id role to admin."""
    await UserManager.change_role(RoleType.ADMIN, user_id)


@router.put(
    '/users/{user_id}/make-approver',
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_approver(user_id: int) -> None:
    """Change user id role to approver."""
    await UserManager.change_role(RoleType.APPROVER, user_id)
