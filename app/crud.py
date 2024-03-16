import datetime

from sqlalchemy.orm import Session

from app import models, schemas


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.uuid == uuid).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_account_by_uuid(db: Session, uuid: str):
    return db.query(models.Account).filter(models.Account.uuid == uuid).first()


def get_services_by_account_uuid(db: Session, account_uuid: str):
    return db.query(models.Account).filter(models.Account.uuid == account_uuid).first().services


def create_service(db: Session, service_data: schemas.ServiceCreate, account_uuid: str):
    service = models.Service(**service_data.dict(), account_uuid=account_uuid)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_all_appointments_between(db: Session, start: datetime.datetime, end: datetime.datetime):
    return db.query(models.Appointment).filter(models.Appointment.date.between(start, end)).all()
