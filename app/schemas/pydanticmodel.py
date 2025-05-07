import re

from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str
    password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values
    @field_validator("password")
    @classmethod
    def validate_password_number(cls, values: str) -> str:
        if not len(values) >= 10:
            raise ValueError('Пароль должен состоять не менее чем из 10 символов')
        return values

class User_check(BaseModel):
    email: EmailStr
    password: str
