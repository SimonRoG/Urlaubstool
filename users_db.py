from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserDB

DATABASE_URL = "sqlite:///./urlaubstool.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def create_user(user):
    db = SessionLocal()
    user_data = user.dict()
    user_data.pop("id", None)
    db_user = UserDB(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


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


def read_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users


def read_user_by_email(email):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.email == email).first()
    db.close()
    return user
