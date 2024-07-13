from ast import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection
from pydantic import BaseModel, EmailStr
from app.dependecies import AdminDep, DBDep, get_id
from app.db import get_db
from psycopg.rows import class_row

router = APIRouter(prefix="/categories")


class CategoryDB(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CategoryReq(BaseModel):
    name: str


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


@router.post("/")
def add_category(category: CategoryReq, conn: DBDep, is_admin: AdminDep):
    print(category.name)
    with conn.cursor(row_factory=class_row(CategoryDB)) as curr:
        existing_record: CategoryDB = curr.execute(
            "SELECT * FROM categories WHERE name = %s", [category.name]
        ).fetchone()
        print(existing_record)
        if existing_record:
            raise HTTPException(status_code=400, detail="category already exists")

        record: CategoryDB = curr.execute(
            "insert into categories (name) values (%s) returning *", [category.name]
        ).fetchone()
        conn.commit()
        print(record)
        return record
