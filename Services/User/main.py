from fastapi import FastAPI
from pydantic import BaseModel
from users_db import create_user, read_user, update_user, delete_user, read_users

app = FastAPI()


class User(BaseModel):
    name: str = "name"
    email: str = "email@email.com"
    password: str = "password"
    role: str = "employee"
    admin: bool = False


@app.get("/users/")
def get_users():
    return {"users": read_users()}


@app.post("/users/", status_code=201)
def post_user(user: User):
    return create_user(user)


@app.get("/users/{id}")
def get_user(id: int):
    return read_user(id)


@app.put("/users/{id}")
def put_user(id: int, user: User):
    return update_user(id, user)


@app.delete("/users/{id}")
def delete_user_route(id: int):
    return delete_user(id)
