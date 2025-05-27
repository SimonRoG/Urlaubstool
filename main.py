from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

class Request(BaseModel):
    id: int
    id: int
    status: str
    date_begin: str
    date_end: str
    date_created: str

users: User = []

requests: Request = []

@app.get("/")
def read_root():
    return {"main": "main"}

@app.get("/users/")
def read_users():
    return {"users": users}

@app.post("/users/", status_code=201)
def create_user(user: User):
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
    return {"requests": requests}

@app.post("/requests/", status_code=201)
def create_request(request: Request):
    requests.append(request)
    return {"message": "Request created successfully", "request": request}

@app.get("/requests/{id}")
def read_request(id: int):
    for request in requests:
        if request.id == id:
            return {"request": request}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/requests/{id}")
def update_request(id: int, request: Request):
    for index, existing_request in enumerate(requests):
        if existing_request.id == id:
            requests[index] = request
            return {"message": "Request updated successfully", "request": request}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/requests/{id}")
def delete_request(id: int):
    for index, request in enumerate(requests):
        if request.id == id:
            del requests[index]
            return {"message": "Request deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

