from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import database_path
from models import Base, UserDB
import httpx

DATABASE_URL = database_path
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def read_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users


def create_user(user):
    user_data = user.dict()

    url = "http://127.0.0.1:8001/register"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "login": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
    }
    response = httpx.post(url, headers=headers, json=data).json()

    return (
        {"response": response, "user": user_data}
        if response.get("user_id")
        else {"error": response.get("detail")}
    )


def read_user(id):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == id).first()
    db.close()
    return user


def update_user(id, user):
    db = SessionLocal()
    db_user = db.query(UserDB).filter(UserDB.id == id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    db.close()
    return db_user


def delete_user(id):
    db = SessionLocal()
    db_user = db.query(UserDB).filter(UserDB.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    db.close()
    return db_user
