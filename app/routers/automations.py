from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db
from app.auth import get_user_and_check_account


automations = APIRouter()


@automations.post('/{account_uuid}/create')
def create_automation(
    account_uuid: str,
    automation: schemas.AutomationCreate,
    current_user: models.User = Depends(get_user_and_check_account),
    db: Session = Depends(get_db),
):
    return crud.create_automation(db, automation, current_user.uuid)


@automations.get('/{account_uuid}/list')
def list_automations(
    account_uuid: str,
    current_user: models.User = Depends(get_user_and_check_account),
    db: Session = Depends(get_db),
):
    return crud.get_automations_by_account_uuid(db, account_uuid)


@automations.patch('/{account_uuid}/enable')
def enable_automation(
    account_uuid: str,
    automation_uuid: str,
    current_user: models.User = Depends(get_user_and_check_account),
    db: Session = Depends(get_db),
):
    return crud.enable_automation(db, automation_uuid)


@automations.patch('/{account_uuid}/disable')
def disable_automation(
    account_uuid: str,
    automation_uuid: str,
    current_user: models.User = Depends(get_user_and_check_account),
    db: Session = Depends(get_db),
):
    return crud.disable_automation(db, automation_uuid)
