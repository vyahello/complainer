"""Provide API schemes."""
# pylint: disable=too-few-public-methods, no-name-in-module
from pydantic import BaseModel


class UserBase(BaseModel):
    """Represents user model schema."""

    email: str


class BaseComplaint(BaseModel):
    """Represents base complaint scheme."""

    title: str
    description: str
    amount: float
