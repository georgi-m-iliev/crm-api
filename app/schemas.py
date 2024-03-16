import datetime

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
    uuid: str
    is_active: bool

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    date: datetime.datetime


class AppointmentCreate(AppointmentBase):
    client_uuid: str
    service_uuid: str


class Appointment(AppointmentBase):
    uuid: str
    client: Client
    service: Service

    class Config:
        from_attributes = True


class AvailabilityRequest(BaseModel):
    service_uuid: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class AppointmentsBetweenRequest(BaseModel):
    start_date: datetime.datetime
    end_date: datetime.datetime
