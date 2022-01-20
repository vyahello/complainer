"""List of useful third-party functionalities."""
import base64

from fastapi import HTTPException


def decode_photo(path: str, encoded_string: str) -> None:
    """Decode user photo."""
    with open(path, 'wb') as file:
        try:
            file.write(base64.b64decode(encoded_string.encode('utf-8')))
        except Exception as exp:
            raise HTTPException(400, 'Invalid photo encoding') from exp
