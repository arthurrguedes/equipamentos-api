from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str