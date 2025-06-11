from jose import JWTError, jwt
import secrets
from datetime import datetime, timedelta

SECRET_KEY = "fjkdghkhdhfjewkhuiyt7855yewuhr3oiy4f78j46hr7238okcyrewo8703R32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token():
    return secrets.token_urlsafe(32)
