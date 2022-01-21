"""Wise payment service API."""
from http.client import HTTPException
from typing import List

import requests
from decouple import config


class WiseService:  # pylint: disable=too-few-public-methods
    """Represents wise payment service."""

    def __init__(self) -> None:
        self.main_url = '...'
        self.headers = {
            'ContentType': 'application/json',
            'Authorization': f'Bearer {config("WISE_TOKEN")}',
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self) -> List[str]:
        """Return wise user profile id"""
        url = 'https://api.sandbox.transferwise.tech/v1/profiles'
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return [
                element['id']
                for element in resp.json()
                if element['type'] == 'personal'
            ][0]
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )
