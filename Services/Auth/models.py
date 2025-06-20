from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from datetime import date

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    passwordHash = Column(String)
    refreshToken = Column(String)
    refreshTokenExpTime = Column(DateTime)
    manager = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)