from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read():
    return {
        "message": "Hello World"
    }
    
@app.get("/items/{item}")
def read(item,q=None):
    return {
        "message": "success",
        "data":{
            "id":item,
            "q":q
        }
    }