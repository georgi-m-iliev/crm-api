import datetime
import random

from sqlalchemy.orm import Session
from twilio.rest import Client
import twilio.base.exceptions
from app.config import settings

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


def get_client(db: Session, name: str, phone: str):
    client = db.query(models.Client).filter(models.Client.name == name, models.Client.phone == phone).first()
    if client is None:
        client = models.Client(name=name, phone=phone)
        db.add(client)

    client.otp_code = str(random.randint(10000, 99999))
    db.commit()
    db.refresh(client)

    twilio = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    try:
        message = twilio.messages.create(
            from_='+18582520393',
            to=client.phone,
            body=f'Your OTP code for AppointMate is {client.otp_code}'
        )
        print(message.sid)
    except twilio.base.exceptions.TwilioRestException:
        print('Error sending OTP code')

    return client


def create_appointment(db: Session, appointment_data: schemas.AppointmentCreate):
    appointment = models.Appointment(**appointment_data.dict())
    if appointment.client.otp_code != appointment_data.otp_code:
        raise ValueError('Invalid OTP code')
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointments_between(db: Session, appointments_request: schemas.AppointmentsBetweenRequest):
    return db.query(models.Appointment).filter(
        models.Appointment.date.between(appointments_request.start_date, appointments_request.end_date)
    ).all()
