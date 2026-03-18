from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(body: ContactCreate, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.create_contact(body)


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    first_name: str | None = Query(default=None, description="Пошук за іменем"),
    last_name: str | None = Query(default=None, description="Пошук за прізвищем"),
    email: str | None = Query(default=None, description="Пошук за email"),
    db: Session = Depends(get_db),
):
    service = ContactService(db)
    return service.get_contacts(first_name=first_name, last_name=last_name, email=email)


@router.get("/upcoming-birthdays", response_model=list[ContactResponse])
def get_upcoming_birthdays(
    days: int = Query(default=7, ge=1, le=30, description="Кількість днів наперед"),
    db: Session = Depends(get_db),
):
    service = ContactService(db)
    return service.get_upcoming_birthdays(days=days)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.get_contact(contact_id)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.update_contact(contact_id, body)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    service = ContactService(db)
    service.delete_contact(contact_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
