"""Provide complaint request output API schemes."""
# pylint: disable=too-few-public-methods

from datetime import datetime

from complainer.models import State
from complainer.schemas.base import BaseComplaint


class ComplaintOut(BaseComplaint):
    """Represents complaint output scheme."""

    id: int  # pylint: disable=invalid-name # noqa
    created_at: datetime
    status: State