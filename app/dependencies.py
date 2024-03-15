from typing import Annotated

from fastapi import Header, HTTPException

from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
