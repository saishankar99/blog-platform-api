from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config import settings
from jose import jwt,JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> models.User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email=payload.get("sub")
        if email is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    User=db.query(models.User).filter(models.User.email==email).first()
    if User is None:
        raise credential_exception
    return User


    