"""Provide API for complaint manager."""
from typing import Dict, List

from databases.backends.postgres import Record
from sqlalchemy.sql import Select

from complainer.db import database
from complainer.models import RoleType, State, complaint


class ComplaintManager:
    """Represents complaint manager."""

    @staticmethod
    async def get_complaints(user: Dict[str, str]) -> List[Record]:
        """Fetch all user complaints."""
        query: Select = complaint.select()
        if user['role'] == RoleType.COMPLAINER:
            query = query.where(complaint.c.id == user['id'])
        elif user['role'] == RoleType.APPROVER:
            query = query.where(complaint.c.state == State.PENDING)
        return await database.fetch_all(query)  # type: ignore

    @staticmethod
    async def create_complaint(
        complaint_data: Dict[str, str], user: Dict[str, str]
    ) -> Record:
        """Fetch one user complaint."""
        complaint_data['complainer_id'] = user['id']
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(  # type: ignore
            complaint.select().where(complaint.c.id == id_)
        )
