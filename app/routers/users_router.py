from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection
from pydantic import BaseModel, EmailStr
from app.dependecies import get_id
from app.db import get_db
from psycopg.rows import class_row

router = APIRouter(prefix="/users")


class UserDB(BaseModel):
    id: int
    email: EmailStr


@router.get("/me")
def me(id: str = Depends(get_id), conn: Connection = Depends(get_db)):
    with conn.cursor(row_factory=class_row(UserDB)) as curr:

        record: UserDB = curr.execute(
            "select * from users where id = %s", [id]
        ).fetchone()
        print(record)
        if not record:
            raise HTTPException(status_code=404, detail="user not found")

        return record
