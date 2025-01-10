#from .config import engine
#from .models import Login

# Create tables
#Login.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.api.controllers import users_controller

app = FastAPI()

app.include_router(users_controller.router)
