from ast import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection
from pydantic import BaseModel, EmailStr
from app.dependecies import DBDep, get_id
from app.db import get_db
from psycopg.rows import class_row

router = APIRouter(prefix="/categories")


class CategoryDB(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


@router.get("/")
def all(conn: DBDep):
    with conn.cursor(row_factory=class_row(CategoryDB)) as curr:
        record: List[CategoryDB] = curr.execute("select * from categories").fetchall()
        print(record)
        return record


@router.get("/{id}")
def category(id: int, conn: DBDep):
    with conn.cursor(row_factory=class_row(CategoryDB)) as curr:
        record: CategoryDB = curr.execute(
            "select * from categories where id = %s", [id]
        ).fetchone()
        print(record)
        return record
