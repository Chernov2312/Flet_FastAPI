from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_session

from app.schemas.pydanticmodel import User
from app.database.engine import session_maker
from app.database.models import Users


async def add_user(session: AsyncSession, data: User):
    obj = Users(
        first_name=data.first_name,
        second_name=data.second_name,
        email=data.email,
        phone_number=data.phone_number,
        password=data.password,
    )
    session.add(obj)
    await session.commit()


async def get_all_users(session: AsyncSession):
    query = select(Users)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user(session: AsyncSession, Users_id: int):
    query = select(Users).where(Users.id == Users_id)
    result = await session.execute(query)
    return result.scalar()


async def update_user(session: AsyncSession, data: User):
    query = update(Users).where(Users.id == data.id).values(
        title=data.title,
        description=data.description,
        completed=data.completed,
    )
    await session.execute(query)
    await session.commit()


async def delete_all_user(session: AsyncSession):
    query = delete(Users)
    await session.execute(query)
    await session.commit()


async def delete_id_user(session: AsyncSession, id: int):
    query = delete(Users).where(Users.id == id)
    await session.execute(query)
    await session.commit()


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session
