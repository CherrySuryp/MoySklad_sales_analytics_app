from typing import Annotated
from fastapi import Header,Request, HTTPException, status
from app.config import settings


async def check_api_token(x_api_token: Annotated[str | None, Header()], request: Request):
    print(request.client.host)
    if x_api_token != settings.API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong API access token"
        )
