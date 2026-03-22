from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    is_admin: bool

    model_config = {"from_attributes": True}
