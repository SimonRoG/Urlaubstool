from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from datetime import date

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    passwordHash = Column(String)
    role = Column(String, default="employee")
    admin = Column(Boolean, default=False)

class UrlaubRequestDB(Base):
    __tablename__ = "urlaub_requests"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(String, default="pending")
    date_begin = Column(Date)
    date_end = Column(Date)
    date_created = Column(Date, default=date.today)