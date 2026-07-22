from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config import settings
from jose import jwt

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expiry_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)