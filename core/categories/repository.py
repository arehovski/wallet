from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.repository import Repository
from settings.db import get_async_session


class CategoryRepository(Repository):
    pass


def get_category_repository(session: AsyncSession = Depends(get_async_session)):
    yield CategoryRepository(session)
