"""Users API scheme validation."""
# pylint: disable=too-few-public-methods, no-name-in-module
from complainer.schemas.base import UserBase


class UserRegisterIn(UserBase):
    """Represents user register schema."""

    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class UserLogin(UserBase):
    """Represents user login schema."""

    password: str
