"""Provide API complaints routes."""
from typing import List

from databases.backends.postgres import Record
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from complainer.managers.auth import (
    is_admin,
    is_approver,
    is_complainer,
    oauth2_scheme,
)
from complainer.managers.complaint import ComplaintManager
from complainer.schemas.request.complaint import ComplaintIn
from complainer.schemas.response.complaint import ComplaintOut

router = APIRouter(tags=['Complaints API'])


@router.get(
    '/complaints',
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[ComplaintOut],
)
async def get_complaints(request: Request) -> List[Record]:
    """Return all user complaints."""
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post(
    '/complaints',
    dependencies=[Depends(oauth2_scheme), Depends(is_complainer)],
    response_model=ComplaintOut,
)
async def create_complaint(request: Request, complaint: ComplaintIn) -> Record:
    """Return a single complaints."""
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(), user)


@router.delete(
    '/complaint/{complaint_id}',
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def delete_complaint(complaint_id: int) -> None:
    """Delete a single complaint."""
    await ComplaintManager.delete(complaint_id)


@router.put(
    '/complaints/{complaint_id}/approve',
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def approve_complaint(complaint_id: int) -> None:
    """Approve user complaint."""
    await ComplaintManager.approve(complaint_id)


@router.put(
    '/complaints/{complaint_id}/reject',
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def reject_complaint(complaint_id: int) -> None:
    """Reject user complaint."""
    await ComplaintManager.reject(complaint_id)
