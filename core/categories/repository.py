from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.categories.exceptions import CategoryAlreadyExists
from core.categories.models import Category
from core.categories.schemas import CategoryCreate
from core.users.models import User
from settings.db import get_async_session


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CategoryCreate, user: User):
        query = (
            select(Category)
            .where(Category.user_id == user.id)
            .where(Category.name == data.name)
        )
        result = await self.session.execute(query)
        existing_category = result.first()
        if existing_category:
            raise CategoryAlreadyExists()

        create_dict = data.dict()
        create_dict["user_id"] = user.id
        category = Category(**create_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category


def get_category_repository(session: AsyncSession = Depends(get_async_session)):
    yield CategoryRepository(session)
