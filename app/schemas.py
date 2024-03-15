from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: str
    is_active: bool
    account: Account

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    uuid: str
    is_active: bool
    users: User

    class Config:
        orm_mode = True
