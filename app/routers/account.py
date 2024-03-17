import pytz
import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db
from app.auth import get_user_and_check_account

account = APIRouter()


@account.get("/{account_uuid}", response_model=schemas.Account)
async def read_account(
    account_uuid: str,
    db: Session = Depends(get_db)
):
    return crud.get_account_by_uuid(db, account_uuid)


@account.get("/{account_uuid}/services", response_model=list[schemas.Service], )
async def read_services(
    account_uuid: str,
    db: Session = Depends(get_db)
):
    return crud.get_services_by_account_uuid(db, account_uuid)


@account.patch("/{account_uuid}/services")
async def create_service(
    account_uuid: str,
    update: schemas.ServicesUpdate,
    user: models.User = Depends(get_user_and_check_account),
    db: Session = Depends(get_db)
):
    return crud.update_services(db, update, account_uuid)


@account.get("/{account_uuid}/availability")
async def get_availability(
    account_uuid: str,
    availability_request: schemas.AvailabilityRequest = Depends(),
    db: Session = Depends(get_db)
):

    existing_appointments = crud.get_all_appointments_between(
        db, availability_request.start_date, availability_request.end_date, account_uuid
    )

    START_HOUR = 8
    END_HOUR = 12
    INTERVAL = 30

    # generate all possible time slots
    timeslots = []
    dates = []

    service = crud.get_service_by_uuid(db, availability_request.service_uuid)

    for day in range((availability_request.end_date - availability_request.start_date).days + 1):
        date = availability_request.start_date + datetime.timedelta(days=day)
        date_time = datetime.datetime(date.year, date.month, date.day).replace(tzinfo=pytz.UTC)
        dates.append(date)
        for hour in range(START_HOUR, END_HOUR):
            for minute in range(0, 60, INTERVAL):
                timeslots.append(
                    {
                        'start': date_time.replace(hour=hour, minute=minute),
                        'end': date_time.replace(hour=hour, minute=minute) + datetime.timedelta(minutes=service.duration)
                    }
                )

    for appointment in existing_appointments:
        appointment_start = appointment.date
        appointment_end = appointment.date + datetime.timedelta(minutes=appointment.service.duration)
        for timeslot in timeslots:
            if timeslot['start'] <= appointment_start < timeslot['end'] \
                    or timeslot['start'] < appointment_end <= timeslot['end']:
                timeslots.remove(timeslot)

    return {
        date:
            [start_end_dates for start_end_dates in timeslots if start_end_dates['start'].date() == date]
        for date in dates
    }
