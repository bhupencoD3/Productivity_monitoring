#import os
#from dotenv import load_dotenv

#load_dotenv()

#class Settings:
 #   SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")

#settings = Settings()
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://username:password@localhost/user_management"

    class Config:
        env_file = ".env"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://username:password@localhost/dbname")

engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

