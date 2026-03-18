from datetime import date, timedelta

from sqlalchemy import extract, or_, select
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contacts(self, first_name: str | None = None, last_name: str | None = None, email: str | None = None) -> list[Contact]:
        stmt = select(Contact)

        filters = []
        if first_name:
            filters.append(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            filters.append(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        if filters:
            stmt = stmt.where(or_(*filters))

        stmt = stmt.order_by(Contact.last_name.asc(), Contact.first_name.asc())
        return list(self.db.scalars(stmt).all())

    def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        return self.db.scalar(stmt)

    def get_contact_by_email(self, email: str) -> Contact | None:
        stmt = select(Contact).where(Contact.email == email)
        return self.db.scalar(stmt)

    def create_contact(self, body: ContactCreate) -> Contact:
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def update_contact(self, contact: Contact, body: ContactUpdate) -> Contact:
        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete_contact(self, contact: Contact) -> None:
        self.db.delete(contact)
        self.db.commit()

    def get_upcoming_birthdays(self, days: int = 7) -> list[Contact]:
        today = date.today()
        future_days = [today + timedelta(days=offset) for offset in range(days + 1)]
        month_day_pairs = {(day.month, day.day) for day in future_days}

        conditions = [
            (extract("month", Contact.birthday) == month) & (extract("day", Contact.birthday) == day)
            for month, day in month_day_pairs
        ]

        stmt = select(Contact).where(or_(*conditions)).order_by(extract("month", Contact.birthday), extract("day", Contact.birthday))
        return list(self.db.scalars(stmt).all())
