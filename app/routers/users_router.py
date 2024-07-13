from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.dependecies import AuthDep, DBDep
from psycopg.rows import class_row

router = APIRouter(prefix="/users")


class UserDB(BaseModel):
    id: int
    email: EmailStr


@router.get("/me")
def me(id: AuthDep, conn: DBDep):
    with conn.cursor(row_factory=class_row(UserDB)) as curr:

        record: UserDB = curr.execute(
            "select * from users where id = %s", [id]
        ).fetchone()
        print(record)
        if not record:
            raise HTTPException(status_code=404, detail="user not found")

        return record


@router.get("/")
def all(conn: DBDep):
    with conn.cursor(row_factory=class_row(UserDB)) as curr:

        record: UserDB = curr.execute(
            "select * from users where is_admin = true"
        ).fetchall()
        print(record)
        return record


@router.get("/{id}")
def user(id: int, conn: DBDep):
    with conn.cursor(row_factory=class_row(UserDB)) as curr:
        record: UserDB = curr.execute(
            "select * from users where id = %s", [id]
        ).fetchone()
        print(record)
        return record
