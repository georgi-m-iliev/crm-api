from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import UUID


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

    @field_validator("uuid")
    def convert_uuid(cls, value, values):
        if isinstance(value, UUID):
            return str(value)
        return value

    class Config:
        from_attributes = True
