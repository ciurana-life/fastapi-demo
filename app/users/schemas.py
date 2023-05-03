from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    editable_field: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    editable_field: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
