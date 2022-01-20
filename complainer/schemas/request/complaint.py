"""Provide complaint request input API schemes."""
# pylint: disable=too-few-public-methods
from complainer.schemas.base import BaseComplaint


class ComplaintIn(BaseComplaint):
    """Represents complaint input scheme."""

    encoded_photo: str
    extension: str
