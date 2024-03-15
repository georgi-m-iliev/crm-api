from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, UUID, DateTime
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
    service = relationship("Service", backref="services")
