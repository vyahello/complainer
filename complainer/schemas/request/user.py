"""Users API scheme."""
# pylint: disable=too-few-public-methods, no-name-in-module
from pydantic import BaseModel


class UserBase(BaseModel):
    """Represents user model schema."""

    email: str


class UserRegisterIn(UserBase):
    """Represents user register schema."""

    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class UserLogin(BaseModel):
    """Represents user login schema."""

    password: str
