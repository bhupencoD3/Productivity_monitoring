from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, dao, dependencies

router = APIRouter()

@router.post("/users/", response_model=schemas.LoginCreate)
def create_user(user: schemas.LoginCreate, db: Session = Depends(dependencies.get_db)):
    db_user = dao.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dao.create_user(db=db, user=user)

