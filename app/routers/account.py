from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db

account = APIRouter()


@account.get("/{account_uuid}", response_model=schemas.Account)
async def read_account(account_uuid: str, db: Session = Depends(get_db)):
    return crud.get_account_by_uuid(db, account_uuid)


@account.get("/{account_uuid}/services", response_model=list[schemas.Service])
async def read_services(account_uuid: str, db: Session = Depends(get_db)):
    return crud.get_services_by_account_uuid(db, account_uuid)


@account.post("/{account_uuid}/services/add", response_model=schemas.Service)
async def create_service(account_uuid: str, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, service, account_uuid)


@account.get("/{account_uuid}/availability")
async def get_availability(
    account_uuid: str, availability_request: schemas.AvailabilityRequest,
    db: Session = Depends(get_db)
):

    existing_appointments = crud.get_all_appointments_between(
        db, availability_request.start_date, availability_request.end_date
    )

    print(existing_appointments)
    print(existing_appointments[0].client.name)
    print(existing_appointments[0].service.duration)

    return {
        '2023-03-17': [
            {
                'start': '2023-03-17 09:00:00',
                'end': '2023-03-17 9:30:00'
            },
            {
                'start': '2023-03-17 10:00:00',
                'end': '2023-03-17 10:30:00'
            },
            {
                'start': '2023-03-17 13:00:00',
                'end': '2023-03-17 13:30:00'
            },
            {
                'start': '2023-03-17 15:00:00',
                'end': '2023-03-17 15:30:00'
            }
        ]
    }
