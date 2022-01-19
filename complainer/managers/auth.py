"""Provide API for user authentication."""
from datetime import datetime, timedelta
from typing import Optional

import jwt
from databases.backends.postgres import Record
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from complainer.db import database
from complainer.models import user


class AuthManager:
    """Represents the client authentication manager."""

    @staticmethod
    def encode_token(input_user: Record) -> str:
        """Encode user's token."""
        payload = {
            'sub': input_user['id'],
            'exp': datetime.utcnow() + timedelta(minutes=120),
        }
        return jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')


class CustomHTTPBearer(HTTPBearer):
    """Represents the http bearer authentication."""

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        """Returns user's bearer credentials."""
        result = await super().__call__(request)

        try:
            payload = jwt.decode(
                result.credentials,  # type: ignore
                config('SECRET_KEY'),
                algorithms=['HS256'],
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload['sub'])
            )
            request.state.user = user_data
            return user_data  # type: ignore
        except jwt.ExpiredSignatureError as exp:
            raise HTTPException(401, 'Token expired') from exp
        except jwt.InvalidTokenError as exp:
            raise HTTPException(401, 'Invalid token') from exp
