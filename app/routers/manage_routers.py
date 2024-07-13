from fastapi import APIRouter, BackgroundTasks
from app.db import get_conn
from faker import Faker
import random
import bcrypt

router = APIRouter(prefix="/manage")

fake = Faker()


def create_fake_data():
    try:
        with get_conn() as conn:
            hashed_password = bcrypt.hashpw(b"123456789", bcrypt.gensalt())
            # Create admin user
            conn.execute(
                """
                INSERT INTO users (email, password, is_admin)
                VALUES (%s, %s, %s)
            """,
                ("admin@admin.com", hashed_password, True),
            )
            # Create random users
            for _ in range(10):
                email = fake.email()
                conn.execute(
                    """
                    INSERT INTO users (email, password)
                    VALUES (%s, %s)
                """,
                    (email, hashed_password),
                )
            # Create random categories
            for _ in range(4):
                category_name = fake.word()
                conn.execute(
                    """
                    INSERT INTO categories (name)
                    VALUES (%s)
                    RETURNING id
                """,
                    (category_name,),
                )
            # Create random posts
            for _ in range(20):
                user_id = fake.random_int(min=1, max=11)
                category_id = fake.random_int(min=1, max=4)
                title = fake.sentence()
                content = fake.paragraphs()
                status = random.choice(["draft", "private", "published"])
                conn.execute(
                    """
                    INSERT INTO posts (user_id, category_id, title, content, status)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (user_id, category_id, title, content, status),
                )

    except Exception as e:
        print(f"An error occurred: {e}")


@router.get("/ping")
def ping():
    with get_conn() as conn:
        record = conn.execute("select 1").fetchone()
        print(record)
        return "pong"


@router.get("/fake-data")
def load_fake_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(create_fake_data)
    return "Fake data loaded"
