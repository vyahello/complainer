"""Provide user response output API schemes."""
# pylint: disable=too-few-public-methods
from complainer.models import RoleType
from complainer.schemas.base import UserBase


class UserOut(UserBase):
    """Represents user output scheme."""

    id: int  # pylint: disable=invalid-name # noqa
    first_name: str
    last_name: str
    phone: str
    role: RoleType
    iban: str
