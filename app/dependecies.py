from typing import Annotated
import jwt as pyjwt
from psycopg import Connection
from psycopg.rows import class_row
from app.config import get_settings
from app.db import get_db

settings = get_settings()

from fastapi import Cookie, Depends, HTTPException

DBDep = Annotated[Connection, Depends(get_db)]


def get_id(jwt: Annotated[str | None, Cookie()] = None):
    print(jwt)
    if not jwt:
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        payload = pyjwt.decode(jwt, settings.jwt_secret, algorithms="HS256")
        print(payload)
        return payload["sub"]
    except Exception as e:
        print(e, "this is error")
        raise HTTPException(status_code=401, detail="not authenticated")


def is_admin(jwt: Annotated[str | None, Cookie()] = None, conn: DBDep = None):
    print(jwt)
    if not jwt:
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        payload = pyjwt.decode(jwt, settings.jwt_secret, algorithms="HS256")
        print(payload)
        id = payload["sub"]
        print(id)
        with conn.cursor() as curr:
            record = curr.execute(
                "select is_admin from users where id = %s and is_admin = true", [id]
            ).fetchone()
            print(record)
            if not record:
                raise HTTPException(status_code=403, detail="unauthorized")
    except pyjwt.PyJWTError as e:
        print(e, "this is error")
        raise HTTPException(status_code=401, detail="not authenticated")


AuthDep = Annotated[str, Depends(get_id)]
AdminDep = Annotated[bool, Depends(is_admin)]
