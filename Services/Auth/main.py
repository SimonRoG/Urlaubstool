from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import database
import hash
import tokens
from models import UserDB

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class RegisterData(BaseModel):
    login : str
    password : str
    name : str
    manager : bool
    admin: bool

class LoginData(BaseModel):
    login : str
    password : str

class RefreshData(BaseModel):
    refreshToken : str

@app.get('/', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/register')
def register(data : RegisterData):
    user = database.get_user_by_login(data.login)
    if (user):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = hash.hash_password(data.password)

    db = database.SessionLocal()
    access_token = tokens.create_access_token(data={"id": database.get_last_user_id() + 1})
    refresh_token = tokens.create_refresh_token()
    new_user = UserDB(email=data.login, passwordHash=hashed_pw, name=data.name, refreshToken=refresh_token, refreshTokenExpTime=datetime.utcnow() + timedelta(days=7), admin=data.admin, manager=data.manager)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    response = JSONResponse(content={"user_id": new_user.id, "access_token": access_token})
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="Lax")
    return response

@app.post('/login')
def login(data: LoginData):
    user = database.get_user_by_login(data.login)
    if not user:
        raise HTTPException(status_code=400, detail="user does not exist")

    if not hash.verify_password(data.password, user.passwordHash):
        raise HTTPException(status_code=400, detail="WrongPassword")

    access_token = tokens.create_access_token(data={"id": user.id})
    refresh_token = tokens.create_refresh_token()
    database.update_user_refreshToken(user.id, refresh_token)

    response = JSONResponse(content={"user_id": user.id, "access_token": access_token})
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="Lax")
    return response

@app.post('/refresh')
def refresh(data : RefreshData):
    user = database.get_user_by_refresh_token(data.refreshToken)
    if not user:
        raise HTTPException(status_code=400, detail="wrong refresh token")
    
    if user.refreshTokenExpTime < datetime.utcnow():
        raise HTTPException(status_code=400, detail="expired refresh token")
    
    refresh_token = tokens.create_refresh_token()
    refresh_responce = database.update_user_refreshToken(user.id, refresh_token)
    if not refresh_responce:
        raise HTTPException(status_code=400, detail="cant update refresh token")
    
    access_token = tokens.create_access_token(data={"id": user.id})

    response = JSONResponse(content={"user_id": user.id, "access_token": access_token})
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="Lax")
    return response