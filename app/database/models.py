from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Users(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[String] = mapped_column(String(50), nullable=False)
    second_name: Mapped[String] = mapped_column(String(50), nullable=False)
    email: Mapped[String] = mapped_column(String(250), nullable=False)
    phone_number: Mapped[String] = mapped_column(String(50), nullable=False)
    password: Mapped[String] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"UserBase(id={self.id}, first_name={self.first_name}, second_name={self.second_name}, email={self.email}, phone_number={self.phone_number}, password={self.password})"