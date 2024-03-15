from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, UUID
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    account_uuid = Column(UUID(as_uuid=True), ForeignKey("accounts.uuid"))

    account = relationship("Account", back_populates="users")


class Account(Base):
    __tablename__ = "accounts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="account")
