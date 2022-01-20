"""Bounder for all API routers."""
from fastapi import APIRouter

from complainer.resources import complaint
from complainer.resources import auth

api_router = APIRouter()
# include already existed router
api_router.include_router(auth.router)
api_router.include_router(complaint.router)
