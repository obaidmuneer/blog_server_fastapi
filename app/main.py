from typing import Union

from fastapi import FastAPI
from app.routers import manage_routers, auth_router

app = FastAPI()
app.include_router(manage_routers.router)
app.include_router(auth_router.router)


@app.get("/")
def read():
    return {"message": "Hello World"}


@app.get("/items/{item}")
def read(item, q=None):
    return {"message": "success", "data": {"id": item, "q": q}}
