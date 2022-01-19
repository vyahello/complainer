"""Provide API schemes."""
# pylint: disable=too-few-public-methods, no-name-in-module
from pydantic import BaseModel


class BaseComplaint(BaseModel):
    """Represents base complaint scheme."""

    title: str
    description: str
    photo_url: str
    amount: float
