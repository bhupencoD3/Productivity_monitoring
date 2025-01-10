#from sqlalchemy.orm import Session
#from app.models.database import get_db
#from app.models.tables import Login

#class UserDAO:
 #   def __init__(self, db: Session = Depends(get_db)):
  #      self.db = db

   # def get_user_by_email(self, email: str):
    #    return self.db.query(Login).filter(Login.email == email, Login.is_deleted == False).first()

from sqlalchemy.orm import Session
from .models import Login
from fastapi import HTTPException

def create_user(db: Session, email: str, password: str, role_id: int):
    db_user = Login(email=email, password=password, role_id=role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(Login).filter(Login.email == email).first()

def update_user(db: Session, user_id: int, password: str):
    db_user = db.query(Login).filter(Login.id == user_id).first()
    if db_user:
        db_user.password = password
        db.commit()
        db.refresh(db_user)
        return db_user
    raise HTTPException(status_code=404, detail="User not found")
