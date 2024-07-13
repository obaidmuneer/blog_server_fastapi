from typing import Annotated
import jwt as pyjwt
from psycopg import Connection
from app.config import get_settings
from app.db import get_db

settings = get_settings()

from fastapi import Cookie, Depends, HTTPException


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


DBDep = Annotated[Connection, Depends(get_db)]
AuthDep = Annotated[str, Depends(get_id)]
