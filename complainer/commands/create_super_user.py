"""Create superuser command API."""
# pylint: disable-all
import asyncclick as click

from complainer.db import database
from complainer.managers.user import UserManager
from complainer.models import RoleType


@click.command()
@click.option('-f', '--first-name', type=str, required=True)
@click.option('-l', '--last-name', type=str, required=True)
@click.option('-e', '--email', type=str, required=True)
@click.option('-p', '--phone', type=str, required=True)
@click.option('-i', '--iban', type=str, required=True)
@click.option('-pa', '--password', type=str, required=True)
async def create_user(
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    iban: str,
    password: str,
) -> None:
    """Create superuser to the database."""
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'iban': iban,
        'password': password,
        'role': RoleType.ADMIN,
    }
    await database.connect()
    await UserManager.register(user_data)  # type: ignore
    await database.disconnect()


if __name__ == '__main__':
    create_user(_anyio_backend='asyncio')
