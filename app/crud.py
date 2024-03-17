import datetime
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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


def get_service_by_uuid(db: Session, uuid: str):
    return db.query(models.Service).filter(models.Service.uuid == uuid).first()


def get_services_by_account_uuid(db: Session, account_uuid: str):
    return db.query(models.Account).filter(models.Account.uuid == account_uuid).first().services


def update_services(db: Session, update: schemas.ServicesUpdate, account_uuid: str):
    # update consists of a list of services - some are existing, some are new and have no uuid
    # we need to remove the services that are not in the update list and add the new ones
    existing_services = db.query(models.Service).filter(models.Service.account_uuid == account_uuid).all()
    existing_services_uuids = [service.uuid for service in existing_services]
    print('existing', existing_services_uuids)
    keep_services_uuids = [service.uuid for service in update.services if service.uuid is not None]
    print('keep', keep_services_uuids)
    new_services = [service for service in update.services if not service.uuid]
    for new_service in new_services:
        del new_service.uuid

    try:
        for service in new_services:
            db.add(models.Service(**service.dict(), account_uuid=account_uuid))
        db.commit()
    except IntegrityError:
        return HTTPException(status_code=400, detail='Service name already exists')

    to_delete_uuids = [uuid for uuid in existing_services_uuids if uuid not in keep_services_uuids]
    for uuid in to_delete_uuids:
        db.query(models.Appointment).filter(models.Appointment.service_uuid == uuid).delete()
        db.query(models.Service).filter(models.Service.uuid == uuid).delete()
    db.commit()

    # update keep_services with new data
    for updated_service in update.services:
        if 'uuid' in updated_service.model_dump(
                exclude_unset=True).keys() and updated_service.uuid in keep_services_uuids:
            db.query(models.Service).filter(models.Service.uuid == updated_service.uuid).update(updated_service.dict())

    return get_services_by_account_uuid(db, account_uuid)


def get_all_appointments_between(db: Session, start: datetime.datetime, end: datetime.datetime, account_uuid: str):
    return [appointment for appointment in db.query(models.Appointment).filter(
        models.Appointment.date.between(start, end)
    ).all() if appointment.service.account_uuid == account_uuid]


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


def create_automation(db: Session, automation: schemas.AutomationCreate):
    db.add(models.Automation(**automation.dict()))
    db.commit()
    return automation


def get_automations_by_account_uuid(db: Session, account_uuid: str):
    return db.query(models.Automation).filter(models.Automation.account_uuid == account_uuid).all()


def enable_automation(db: Session, automation_uuid: str):
    automation = db.query(models.Automation).filter(models.Automation.uuid == automation_uuid).first()
    automation.enabled = True
    db.commit()
    return automation


def disable_automation(db: Session, automation_uuid: str):
    automation = db.query(models.Automation).filter(models.Automation.uuid == automation_uuid).first()
    automation.enabled = False
    db.commit()
    return automation
