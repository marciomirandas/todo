from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User
from schemas.user import UserSchema
from core.security import hash_password, verify_password, create_access_token, pwd_context
from api.deps import get_db, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta


router = APIRouter(prefix="/auth", tags=["auth2"])


@router.post("/register")
async def register(user: UserSchema, db: Session = Depends(get_db)):
    db_user = User(email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    refresh_token = create_access_token({"sub": str(db_user.id)}, timedelta(days=7))

    return {
        "access_token": token,
        "refresh_token": refresh_token
    }


@router.post("/token")
async def login_oauth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/refresh")
def refresh_token(user: User = Depends(get_current_user)):
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
