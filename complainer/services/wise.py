"""Wise payment service API."""
import json
from http.client import HTTPException
from typing import Any, Dict, List

import requests
from decouple import config


class WiseService:  # pylint: disable=too-few-public-methods
    """Represents wise payment service."""

    def __init__(self) -> None:
        self.main_url = config('WISE_URL')
        self.headers = {
            'ContentType': 'application/json',
            'Authorization': f'Bearer {config("WISE_TOKEN")}',
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self) -> List[str]:
        """Return wise user profile id."""
        url = f'{self.main_url}/v1/profiles'
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

    def create_quote(self, amount: int) -> Dict[str, Any]:
        """Create quote in wise payment service."""
        url = f'{self.main_url}/v2/quotes'
        data = {
            'sourceCurrency': 'EUR',
            'targetCurrency': 'EUR',
            'sourceAmount': amount,
            'profile': self.profile_id,
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            return resp.json()
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )
