from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database
import hash
from models import UserDB

app = FastAPI()

class RegisterData(BaseModel):
    login : str
    password : str
    name : str

class LoginData(BaseModel):
    login : str
    password : str

@app.post('/register')
def register(data : RegisterData):
    user = database.get_user_by_login(data.login)
    if (user):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = hash.hash_password(data.password)

    db = database.SessionLocal()
    new_user = UserDB(email=data.login, passwordHash=hashed_pw, name=data.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post('/login')
def login(data : LoginData):
    user = database.get_user_by_login(data.login)
    if (user):
        if hash.verify_password(data.password, user.passwordHash):
            return {"message": "User logined successfully", "user_id": user.id}
        else:
            raise HTTPException(status_code=400, detail="WrongPassword")
    
    raise HTTPException(status_code=400, detail="user does not exist")