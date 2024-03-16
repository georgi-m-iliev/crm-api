from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db

appointments = APIRouter()


@appointments.post('/clients/get', response_model=schemas.Client)
def get_client(client: schemas.ClientBase, db: Session = Depends(get_db)):
    return crud.get_client(db, **client.dict())


@appointments.post('/create', response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appointment)


@appointments.get('/get', response_model=list[schemas.Appointment])
def get_appointments_between(appointments_request: schemas.AppointmentsBetweenRequest, db: Session = Depends(get_db)):
    return crud.get_appointments_between(db, appointments_request)
