from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate


class ContactService:
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)

    def get_contacts(self, first_name: str | None = None, last_name: str | None = None, email: str | None = None) -> list[Contact]:
        return self.repository.get_contacts(first_name=first_name, last_name=last_name, email=email)

    def get_contact(self, contact_id: int) -> Contact:
        contact = self.repository.get_contact_by_id(contact_id)
        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        return contact

    def create_contact(self, body: ContactCreate) -> Contact:
        existing = self.repository.get_contact_by_email(body.email)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact with this email already exists")
        return self.repository.create_contact(body)

    def update_contact(self, contact_id: int, body: ContactUpdate) -> Contact:
        contact = self.get_contact(contact_id)

        if body.email and body.email != contact.email:
            existing = self.repository.get_contact_by_email(body.email)
            if existing is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact with this email already exists")

        return self.repository.update_contact(contact, body)

    def delete_contact(self, contact_id: int) -> None:
        contact = self.get_contact(contact_id)
        self.repository.delete_contact(contact)

    def get_upcoming_birthdays(self, days: int = 7) -> list[Contact]:
        return self.repository.get_upcoming_birthdays(days=days)
