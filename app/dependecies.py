from typing import Annotated
import jwt as pyjwt
from app.config import get_settings

settings = get_settings()

from fastapi import Cookie, HTTPException


def get_id(jwt: Annotated[str | None, Cookie()] = None):
    print(jwt)
    if not jwt:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = pyjwt.decode(jwt, settings.jwt_secret, algorithms="HS256")
        print(payload)
        return payload["sub"]
    except Exception as e:
        print(e, "this is error")
        raise HTTPException(status_code=401, detail="Not authenticated")
