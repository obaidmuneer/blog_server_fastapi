from datetime import datetime, timedelta
import jwt
import bcrypt
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr
from app.db import get_conn
from psycopg.rows import class_row
from app.config import get_settings

settings = get_settings()


class Signin(BaseModel):
    email: EmailStr
    password: str


class Signup(BaseModel):
    username: str
    email: EmailStr
    password: str


router = APIRouter(prefix="/auth")


@router.post("/sign-up")
def sign_up(data: Signup):
    hased_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())
    with get_conn() as conn:
        record = conn.execute(
            "SELECT * FROM users WHERE email = %s", (data.email,)
        ).fetchone()
        if record:
            raise HTTPException(status_code=400, detail="user already exists")
        conn.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (data.email, hased_password.decode("utf-8")),
        )
    return {"message": "success"}


class UserDB(BaseModel):
    id: int
    email: EmailStr
    password: str | None


@router.post("/sign-in")
def login(data: Signin, response: Response):
    with get_conn() as conn, conn.cursor(row_factory=class_row(UserDB)) as curr:
        # hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())

        record: UserDB = curr.execute(
            "select * from users where email = %s", [data.email]
        ).fetchone()
        print(record)
        if not record:
            raise HTTPException(status_code=404, detail="user not found")

        is_password_correct = bcrypt.checkpw(
            data.password.encode("utf-8"), record.password.encode("utf-8")
        )
        if not is_password_correct:
            raise HTTPException(status_code=400, detail="incorrect password")
        expire = datetime.utcnow() + timedelta(minutes=30)
        payload = {"sub": record.id, "exp": expire}
        token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
        response.set_cookie(key="jwt", value=token, httponly=True)

    return {"message": "success"}
