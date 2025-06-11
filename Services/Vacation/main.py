from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import date
from vacations_db import (
    create_request,
    read_request,
    update_request,
    delete_request,
    read_requests,
)

app = FastAPI()


class UrlaubRequest(BaseModel):
    id: int
    user_id: int
    status: str = "pending"
    date_begin: date
    date_end: date
    date_created: date


@app.get("/requests/")
def get_requests():
    return {"requests": read_requests()}


@app.post("/requests/", status_code=201)
async def post_request(
    user_id: int = Form(...), date_begin: str = Form(...), date_end: str = Form(...)
):
    urlaub_request = UrlaubRequest(
        id=0,
        user_id=int(user_id),
        status="pending",
        date_begin=date.fromisoformat(date_begin),
        date_end=date.fromisoformat(date_end),
        date_created=date.today(),
    )
    create_request(urlaub_request)
    return RedirectResponse(url=f"/?id={user_id}", status_code=302)


@app.get("/requests/{id}")
def get_request(id: int):
    return read_request(id)


@app.put("/requests/{id}/{status}")
def put_request(id: int, status: str):
    ureq = read_request(id)

    urlaub_request = UrlaubRequest(
        id=ureq.id,
        user_id=ureq.user_id,
        status=status,
        date_begin=ureq.date_begin,
        date_end=ureq.date_end,
        date_created=ureq.date_created,
    )

    update_request(id, urlaub_request)


@app.delete("/requests/{id}")
def delete_request_route(id: int):
    return delete_request(id)
