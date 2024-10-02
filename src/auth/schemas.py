from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    last_name: str


class CreateUser(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class Auth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str