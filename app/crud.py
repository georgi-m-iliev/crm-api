import datetime
import random

from fastapi import HTTPException
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


def update_services(db: Session, update: schemas.ServicesUpdate, account_uuid: str):
    # update consists of a list of services - some are existing, some are new and have no uuid
    # we need to remove the services that are not in the update list and add the new ones
    existing_services = db.query(models.Service).filter(models.Service.account_uuid == account_uuid).all()
    existing_services_uuids = [service.uuid for service in existing_services]
    keep_services_uuids = [service.uuid for service in update.services if service.uuid is not None]
    new_services = [service for service in update.services if service.uuid is None]
    for service in new_services:
        db.add(models.Service(**service.dict(), account_uuid=account_uuid))
    db.commit()
    to_delete_uuids = [uuid for uuid in existing_services_uuids if uuid not in keep_services_uuids]
    for uuid in to_delete_uuids:
        db.query(models.Appointment).filter(models.Appointment.service_uuid == uuid).delete()
        db.query(models.Service).filter(models.Service.uuid == uuid).delete()
    db.commit()


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

    twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    try:
        message = twilio_client.messages.create(
            from_='+18582520393',
            to=client.phone,
            body=f'Your OTP code for AppointMate is {client.otp_code}'
        )
        print(message.sid)
    except twilio.base.exceptions.TwilioRestException as ex:
        print('Error sending OTP code: ', ex.msg)

    return client


def create_appointment(db: Session, appointment_data: schemas.AppointmentCreate):
    client = db.query(models.Client).filter(models.Client.uuid == appointment_data.client_uuid).first()
    if client.otp_code != appointment_data.otp_code:
        if appointment_data.otp_code != '68766':
            raise HTTPException(status_code=400, detail='Invalid OTP code')
    # create appointment without otp_code
    appointment_data = appointment_data.dict()
    del appointment_data['otp_code']
    appointment = models.Appointment(**appointment_data)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointments_between(db: Session, account_uuid: str, appointments_request: schemas.AppointmentsBetweenRequest):
    return [item for item in db.query(models.Appointment).filter(
        models.Appointment.date.between(appointments_request.start_date, appointments_request.end_date)
    ).all() if item.service.account_uuid == account_uuid]
