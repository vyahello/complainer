"""Wise payment service API."""
import json
import uuid
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

    def create_quote(self, amount: int) -> str:
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

    def create_recipient_account(self, full_name: str, iban: str) -> str:
        """Create recipient account in wise payment service."""
        url = f'{self.main_url}/v1/accounts'
        data = {
            'currency': 'EUR',
            'type': 'iban',
            'profile': self.profile_id,
            'accountHolderName': full_name,
            'legalType': 'PRIVATE',
            'details': {'iban': iban},
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            return resp.json()
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )

    def create_transfer(self, target_account_id: str, quote_id: str) -> str:
        """Create transfer in wise payment service."""
        url = f'{self.main_url}/v1/transfers'
        data = {
            'targetAccount': target_account_id,
            'quoteUuid': quote_id,
            'customerTransactionId': str(uuid.uuid4()),
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 200:
            return resp.json()
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )

    def fund_transfer(
        self,
        transfer_id: int,
    ) -> Dict[str, Any]:
        """Fund transfer in wise payment service."""
        url = (
            f'{self.main_url}/v3/profiles/'
            f'{self.profile_id}/transfers/{transfer_id}/payment'
        )
        data = {'type': 'BALANCE'}
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        if resp.status_code == 201:
            return resp.json()
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )

    def cancel_funds(self, transfer_id: int) -> Dict[str, Any]:
        """Cancel fund transfer in wise payment service."""
        url = f'{self.main_url}/v1/transfer/{transfer_id}/cancel'
        resp = requests.put(url, headers=self.headers)

        if resp.status_code == 200:
            return resp.json()
        raise HTTPException(
            500, 'Payment provider is not available at the moment'
        )
