from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.categories.models import Category
from settings.db import get_async_session


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, create_dict: dict[str, Any]):
        category = Category(**create_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category


def get_category_repository(session: AsyncSession = Depends(get_async_session)):
    yield CategoryRepository(session)
