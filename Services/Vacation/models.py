from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from datetime import date

Base = declarative_base()

class UrlaubRequestDB(Base):
    __tablename__ = "urlaub_requests"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(String, default="pending")
    date_begin = Column(Date)
    date_end = Column(Date)
    date_created = Column(Date, default=date.today)