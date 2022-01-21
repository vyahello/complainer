"""Simple email service (ses) API."""
from typing import List

import boto3
from decouple import config


class SESService:
    """Represents simple email service."""

    BASE_EMAIL = 'vyahello@gmail.com'

    def __init__(
        self,
    ) -> None:
        self.ses = boto3.client(
            'ses',
            region_name=config('SES_REGION'),
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY'),
        )

    def send_email(
        self, subject: str, to_addresses: List[str], text_data: str
    ) -> None:
        """Send email from SES service."""
        body = {'Text': {'Data': text_data, 'Charset': 'UTF-8'}}
        self.ses.send_email(
            Source=self.BASE_EMAIL,
            Destination={
                'ToAddresses': to_addresses,
                'CcAddresses': [],
                'BccAddresses': [],
            },
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': body,
            },
        )
