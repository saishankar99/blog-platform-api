from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import hash_password

router = APIRouter(prefix="/users",tags=['users'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    new_user=models.User(email=user.email,hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user