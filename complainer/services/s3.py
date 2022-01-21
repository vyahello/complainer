"""Simple storage service (s3) API."""
from http.client import HTTPException

import boto3
from decouple import config


class S3Service:
    """Represents simple storage service object."""

    def __init__(
        self,
    ) -> None:
        self.s3 = boto3.client(  # pylint: disable=invalid-name
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY'),
        )
        self.bucket = config('AWS_BUCKET_NAME')
        self.region = config('AWS_REGION')

    def upload(self, path: str, key: str, ext: str) -> str:
        """Upload file to S3 bucket."""
        try:
            self.s3.upload_file(
                path,
                self.bucket,
                key,
                ExtraArgs={'ACL': 'public-read', 'ContentType': f'image/{ext}'},
            )
            return (
                f'https://{self.bucket}.s3.{self.region}.'
                f'amazonaws.com/{key}'
            )
        except Exception as exp:
            raise HTTPException(500, 'S3 is not available') from exp
