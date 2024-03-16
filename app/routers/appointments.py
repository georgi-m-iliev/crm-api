from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db

appointments = APIRouter()


@appointments.get('/clients/get', response_model=schemas.Client)
def get_client(client: schemas.ClientBase, db: Session = Depends(get_db)):
    return crud.get_client(db, **client.dict())
