import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from settings.db import Base, get_async_session

# TODO sqlalchemy rel imports

class User(SQLAlchemyBaseUserTableUUID, Base):
    created: datetime.datetime = Column('created', DateTime, default=datetime.datetime.now, nullable=False)

    categories = relationship("User", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
