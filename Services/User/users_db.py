from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import database_path

DATABASE_URL = database_path
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    passwordHash = Column(String)
    role = Column(String, default="employee")
    admin = Column(Boolean, default=False)


def read_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users


def create_user(user):
    db = SessionLocal()
    user_data = user.dict()
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