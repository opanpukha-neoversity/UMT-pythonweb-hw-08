from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ContactBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100, examples=["Іван"])
    last_name: str = Field(min_length=1, max_length=100, examples=["Петренко"])
    email: EmailStr = Field(examples=["ivan.petrenko@example.com"])
    phone_number: str = Field(min_length=7, max_length=30, examples=["+380671234567"])
    birthday: date = Field(examples=["1999-05-14"])
    additional_data: str | None = Field(default=None, max_length=2000, examples=["Друг з університету"])

    @field_validator("first_name", "last_name", "phone_number")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("The field cannot be empty")
        return value

    @field_validator("birthday")
    @classmethod
    def birthday_cannot_be_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("The date of birth cannot be in the future")
        return value


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=7, max_length=30)
    birthday: date | None = None
    additional_data: str | None = Field(default=None, max_length=2000)

    @field_validator("first_name", "last_name", "phone_number")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("The field cannot be empty")
        return value

    @field_validator("birthday")
    @classmethod
    def optional_birthday_cannot_be_in_future(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("The date of birth cannot be in the future")
        return value


class ContactResponse(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
