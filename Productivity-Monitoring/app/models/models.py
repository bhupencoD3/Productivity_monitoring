from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, nullable=False)
    created_on = Column(TIMESTAMP, default=func.current_timestamp())
    modified_on = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_delete = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Login(email={self.email}, role_id={self.role_id}, created_on={self.created_on})>"
