from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    uuid: str
    is_active: bool

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: str
    is_active: bool

    class Config:
        from_attributes = True
