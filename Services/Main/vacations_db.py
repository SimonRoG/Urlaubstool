from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UrlaubRequestDB 

DATABASE_URL = "sqlite:///./urlaubstool.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def create_request(urlaub_request):
    db = SessionLocal()
    request_data = urlaub_request.dict()
    request_data.pop("id", None)
    db_request = UrlaubRequestDB(**request_data)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    db.close()
    return db_request


def read_request(id):
    db = SessionLocal()
    req = db.query(UrlaubRequestDB).filter(UrlaubRequestDB.id == id).first()
    db.close()
    return req


def update_request(id, urlaub_request):
    db = SessionLocal()
    db_req = db.query(UrlaubRequestDB).filter(UrlaubRequestDB.id == id).first()
    if db_req:
        for key, value in urlaub_request.dict().items():
            setattr(db_req, key, value)
        db.commit()
        db.refresh(db_req)
    db.close()
    return db_req


def delete_request(id):
    db = SessionLocal()
    db_req = db.query(UrlaubRequestDB).filter(UrlaubRequestDB.id == id).first()
    if db_req:
        db.delete(db_req)
        db.commit()
    db.close()
    return db_req


def read_requests(user_id=None):
    db = SessionLocal()
    if user_id:
        reqs = (
            db.query(UrlaubRequestDB).filter(UrlaubRequestDB.user_id == user_id).all()
        )
    else:
        reqs = db.query(UrlaubRequestDB).all()
    db.close()
    return reqs
