from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date

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

users: User = []

urlaub_requests: UrlaubRequest = []

@app.get("/")
def read_root(request: Request, id: int = None):
    user = None
    if id is not None:
        for u in users:
            if u.id == id:
                user = u
                break
    if not user:
        return RedirectResponse(url="/login")
    
    if user.role == "manager":
        user_urlaub_requests = urlaub_requests
    else:
        user_urlaub_requests = [req for req in urlaub_requests if req.user_id == user.id]

    return templates.TemplateResponse("index.html", {"request": request, "users": users, "user": user, "user_urlaub_requests": user_urlaub_requests})

@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    for user in users:
        if user.email == email and user.password == password:
            response = RedirectResponse(url=f"/?id={user.id}", status_code=302)
            return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@app.get("/users/")
def read_users():
    return {"users": users}

@app.post("/users/", status_code=201)
def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="ID already exists")
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    users.append(user)
    return {"message": "User created successfully", "user": user}

@app.get("/users/{id}")
def read_user(id: int):
    for user in users:
        if user.id == id:
            return {"user": user}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/users/{id}")
def update_user(id: int, user: User):
    for index, existing_user in enumerate(users):
        if existing_user.id == id:
            for other_user in users:
                if other_user.id != id:
                    if other_user.id == user.id:
                        raise HTTPException(status_code=400, detail="ID already exists")
                    if other_user.email == user.email:
                        raise HTTPException(status_code=400, detail="Email already exists")
            users[index] = user
            return {"message": "User updated successfully", "user": user}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/users/{id}")
def delete_user(id: int):
    for index, user in enumerate(users):
        if user.id == id:
            del users[index]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/requests/")
def read_requests():
    return {"requests": urlaub_requests}

@app.post("/requests/", status_code=201)
def create_request(urlaub_request: UrlaubRequest):
    urlaub_requests.append(urlaub_request)
    return {"message": "UrlaubRequest created successfully", "urlaub_request": urlaub_request}

@app.get("/requests/{id}")
def read_request(id: int):
    for urlaub_request in urlaub_requests:
        if urlaub_request.id == id:
            return {"urlaub_request": urlaub_request}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/requests/{id}")
def update_request(id: int, urlaub_request: UrlaubRequest):
    for index, existing_urlaub_request in enumerate(urlaub_requests):
        if existing_urlaub_request.id == id:
            urlaub_requests[index] = urlaub_request
            return {"message": "UrlaubRequest updated successfully", "urlaub_request": urlaub_request}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/requests/{id}")
def delete_request(id: int):
    for index, urlaub_request in enumerate(urlaub_requests):
        if urlaub_request.id == id:
            del urlaub_requests[index]
            return {"message": "UrlaubRequest deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

