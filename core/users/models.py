import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from settings.db import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    created: datetime.datetime = Column('created', DateTime, default=datetime.datetime.now)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
