"""Provide API for complaint manager."""
import os
import uuid
from typing import Any, Dict, List

from databases.backends.postgres import Record
from sqlalchemy.sql import Select

from complainer.constants import TEMP_FILE_FOLDER
from complainer.db import database
from complainer.models import RoleType, State, complaint, transaction
from complainer.services.s3 import S3Service
from complainer.services.ses import SESService
from complainer.services.wise import WiseService
from complainer.utils.helpers import decode_photo

s3 = S3Service()
ses = SESService()
wise = WiseService()


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
        complaint_data: Dict[str, Any],
        user: Dict[str, str],
        issue_transaction: bool = False,
    ) -> Record:
        """Fetch one user complaint."""
        complaint_data['complainer_id'] = user['id']
        # s3 integration
        encoded_photo = complaint_data.pop('encoded_photo')
        extension = complaint_data.pop('extension')
        name = f'{uuid.uuid4()}.{extension}'
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data['photo_url'] = s3.upload(path, name, extension)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(complaint_data))
        if issue_transaction:
            await ComplaintManager.issue_transaction(
                complaint_data['amount'],
                f'{user["first_name"]} {user["last_name"]}',
                user['iban'],
                id_,
            )
        return await database.fetch_one(  # type: ignore
            complaint.select().where(complaint.c.id == id_)
        )

    @staticmethod
    async def delete(complaint_id: int) -> None:
        """Delete complaint of a user. Only admin user can delete complaints."""
        await database.execute(
            complaint.delete().where(complaint.c.id == complaint_id)
        )

    @staticmethod
    async def approve(complaint_id: int, fund_transfer: bool = False) -> None:
        """Approve user complaint."""
        await ComplaintManager._apply(complaint_id, State.APPROVED)
        transaction_data = await database.fetch_one(
            transaction.select().where(
                transaction.c.complaint_id == complaint_id
            )
        )
        if fund_transfer:
            wise.fund_transfer(transaction_data['transfer_id'])  # type: ignore
        # ses integration, send email to recipient in case of approval
        ses.send_email(
            subject='Complaint approved',
            to_addresses=['vjagello93@gmail.com'],
            text_data='Congrats! Your claim is approved!',
        )

    @staticmethod
    async def reject(complaint_id: int, fund_transfer: bool = False) -> None:
        """Reject user complaint."""
        transaction_data = await database.fetch_one(
            transaction.select().where(
                transaction.c.complaint_id == complaint_id
            )
        )
        if fund_transfer:
            wise.cancel_funds(transaction_data['transfer_id'])  # type: ignore
        await ComplaintManager._apply(complaint_id, State.REJECTED)

    @staticmethod
    async def issue_transaction(
        amount: int, full_name: str, iban: str, complaint_id: int
    ) -> None:
        """Store transaction into database."""
        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(full_name, iban)
        transfer_id = wise.create_transfer(recipient_id, quote_id)
        data = {
            'quote_id': quote_id,
            'transfer_id': transfer_id,
            'target_account_id': str(recipient_id),
            'amount': amount,
            'complaint_id': complaint_id,
        }
        await database.execute(transaction.insert().values(**data))

    @staticmethod
    async def _apply(complaint_id: int, status: State) -> None:
        """Apply action to user complaint."""
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=status)
        )
