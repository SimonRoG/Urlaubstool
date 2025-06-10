from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import UserDB
from models import Base
import tokens
from settings import database_path

DATABASE_URL = database_path

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_user_by_login(email: str):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.email == email).first()
    db.close()
    return user

def get_user_by_refresh_token(token: str):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.refreshToken == token).first()
    db.close()
    return user

def update_user_refreshToken(id : int, newToken : str):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == id).first()
    if user:
        user.refreshToken = newToken
        user.refreshTokenExpTime = datetime.utcnow() + timedelta(days=7)
        db.commit()
        db.refresh(user)
        db.close()
        return user

    db.close()

def get_last_user_id():
    db = SessionLocal()
    last_user = db.query(UserDB).order_by(UserDB.id.desc()).first()
    db.close()
    if last_user:
        return last_user.id
    else:
        return 0