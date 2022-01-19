"""Provide API for user registration."""
from typing import Dict

from fastapi import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from complainer.db import database
from complainer.managers.auth import AuthManager
from complainer.models import user

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserManager:
    """
    Represents object to manage users (register, save to db)
    and pass it to authentication manager.
    """

    @staticmethod
    async def register(user_data: Dict[str, str]) -> str:
        """
        Register user in the database.
        Return encoded hash.
        """
        user_data['password'] = pwd_context.hash(user_data['password'])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError as exp:
            raise HTTPException(
                400, 'User with this email already exists'
            ) from exp

        user_do = await database.fetch_one(
            user.select().where(user.c.id == id_)
        )
        return AuthManager.encode_token(user_do)  # type: ignore

    @staticmethod
    async def login(user_data: Dict[str, str]) -> str:
        """
        Check if user email exists in the database.
        Return encoded hash.
        """
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data['email'])
        )
        if not user_do:
            raise HTTPException(400, 'Wrong email or password')
        if not pwd_context.verify(
            user_data['password'], user_do['password']  # type: ignore
        ):
            raise HTTPException(400, 'Wrong email or password')
        return AuthManager.encode_token(user_do)  # type: ignore
