from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserDB
from models import Base
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