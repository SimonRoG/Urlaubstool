from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date
from users_db import (
    create_user,
    read_user,
    update_user,
    delete_user,
    read_users,
    read_user_by_email,
)
from vacations_db import (
    create_request,
    read_request,
    update_request,
    delete_request,
    read_requests,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str = "name"
    email: str = "email@email.com"
    password: str = "password"
    role: str = "employee"
    admin: bool = False


class UrlaubRequest(BaseModel):
    id: int
    user_id: int
    status: str = "pending"
    date_begin: date
    date_end: date
    date_created: date


@app.get("/")
def read_root(request: Request, id: int = None):
    user = read_user(id)
    if not user:
        return RedirectResponse(url="/login")

    user_urlaub_requests = (
        read_requests(user.id) if user.role != "manager" else read_requests()
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": read_users(),
            "user": user,
            "user_urlaub_requests": user_urlaub_requests,
        },
    )


@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = read_user_by_email(email)
    if user and user.password == password:
        response = RedirectResponse(url=f"/?id={user.id}", status_code=302)
        return response
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"}
    )


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


@app.get("/requests/")
def get_requests():
    return {"requests": read_requests()}


@app.post("/requests/", status_code=201)
def post_request(urlaub_request: UrlaubRequest):
    return create_request(urlaub_request)


@app.get("/requests/{id}")
def get_request(id: int):
    return read_request(id)


@app.put("/requests/{id}")
def put_request(id: int, urlaub_request: UrlaubRequest):
    return update_request(id, urlaub_request)


@app.delete("/requests/{id}")
def delete_request_route(id: int):
    return delete_request(id)
