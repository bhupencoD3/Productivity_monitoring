from pydantic import BaseModel

class LoginCreate(BaseModel):
    email: str
    password: str
    role_id: int

    class Config:
        orm_mode = True
