from pydantic import BaseModel

# ✅ Request body schema for user registration & login
class CreateUser(BaseModel):
    name: str
    email: str
    password: str

# ✅ Response schema returned after user is created
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True  # allows SQLAlchemy model to work with Pydantic

# ✅ Schema for login (just email & password)
class LoginUser(BaseModel):
    email: str
    password: str