from typing import Annotated
from fastapi import Header, HTTPException, status
from app.config import settings


def check_api_token(x_api_token: Annotated[str | None, Header()]):
    if x_api_token != settings.API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong API access token"
        )
    ...
