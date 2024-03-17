import datetime
from typing import List

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
    account_uuid: str

    class Config:
        from_attributes = True


class ClientBase(BaseModel):
    name: str
    phone: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    uuid: str

    class Config:
        from_attributes = True


class ServiceBase(BaseModel):
    name: str
    duration: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    uuid: str | None
    # is_active: bool

    class Config:
        from_attributes = True


class ServicesCreate(BaseModel):
    services: list[ServiceCreate]


class AppointmentBase(BaseModel):
    date: datetime.datetime


class AppointmentCreate(AppointmentBase):
    client_uuid: str
    service_uuid: str
    otp_code: str


class Appointment(AppointmentBase):
    uuid: str
    client: Client
    service: Service

    class Config:
        from_attributes = True


class AvailabilityRequest(BaseModel):
    service_uuid: str
    start_date: datetime.date
    end_date: datetime.date


class AppointmentsBetweenRequest(BaseModel):
    start_date: datetime.datetime
    end_date: datetime.datetime


class ServicesUpdate(BaseModel):
    services: List[Service]


class AutomationBase(BaseModel):
    name: str
    type: str
    description: str
    is_active: bool
    message: str
    status: str


class AutomationCreate(AutomationBase):
    pass


class Automation(AutomationBase):
    uuid: str
    account_uuid: str

    class Config:
        from_attributes = True
