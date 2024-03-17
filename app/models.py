from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, DateTime, Time
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    account_uuid = Column(String, ForeignKey("accounts.uuid"))

    account = relationship("Account", backref="accounts")


class Account(Base):
    __tablename__ = "accounts"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    services = relationship("Service", backref="services")


class Client(Base):
    __tablename__ = "clients"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    otp_code = Column(String(5), nullable=False)


class Service(Base):
    __tablename__ = "services"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    account_uuid = Column(String, ForeignKey("accounts.uuid"))


class Appointment(Base):
    __tablename__ = "appointments"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    date = Column(DateTime(timezone=True), nullable=False)
    client_uuid = Column(String, ForeignKey("clients.uuid"))
    service_uuid = Column(String, ForeignKey("services.uuid"))

    client = relationship("Client", backref="clients")
    service = relationship("Service", backref="services.uuid")


class Automation(Base):
    __tablename__ = "automations"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    account_uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    message = Column(String, nullable=False)
    status = Column(String, nullable=False)


class AutomationEvent(Base):
    __tablename__ = "automations_events"

    uuid = Column(String, primary_key=True, server_default=func.gen_random_uuid())
    automation_uuid = Column(String, ForeignKey("automations.account_uuid"))
    schedule_time = Column(Time(timezone=True), nullable=False)
    client_uuid = Column(String, ForeignKey("clients.uuid"))
    message = Column(String, nullable=False)
