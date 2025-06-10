from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
import database
import hash
import tokens
from models import UserDB

app = FastAPI()

class RegisterData(BaseModel):
    login : str
    password : str
    name : str

class LoginData(BaseModel):
    login : str
    password : str

class RefreshData(BaseModel):
    refreshToken : str

@app.post('/register')
def register(data : RegisterData):
    user = database.get_user_by_login(data.login)
    if (user):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = hash.hash_password(data.password)

    db = database.SessionLocal()
    access_token = tokens.create_access_token(data={"id": database.get_last_user_id() + 1})
    refresh_token = tokens.create_refresh_token()
    new_user = UserDB(email=data.login, passwordHash=hashed_pw, name=data.name, refreshToken=refresh_token, refreshTokenExpTime=datetime.utcnow() + timedelta(days=7))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    return {"access": access_token, "refresh_token": refresh_token,"user_id": new_user.id}

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

    return {
        "access": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id
    }

@app.post('/refresh')
def refresh(data : RefreshData):
    refresh_token = tokens.create_refresh_token()
    user = database.get_user_by_refresh_token(data.refreshToken)
    if not user:
        raise HTTPException(status_code=400, detail="wrong refresh token")
    
    refresh_responce = database.update_user_refreshToken(user.id, refresh_token)
    if not refresh_responce:
        raise HTTPException(status_code=400, detail="cant update refresh token")
    
    access_token = tokens.create_access_token(data={"id": user.id})

    return {
        "access": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id
    }