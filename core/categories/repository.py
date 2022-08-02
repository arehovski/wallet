from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from core.categories.exceptions import CategoryAlreadyExists, CategoryNotFound
from core.categories.models import Category, CategoryType
from core.categories.schemas import CategoryCreate, CategoryUpdate
from core.users.models import User
from settings.db import get_async_session


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CategoryCreate, user: User) -> Category:
        await self._check_existing_category(data.name, user.id)

        create_dict = data.dict()
        create_dict["user_id"] = user.id
        category = Category(**create_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def categories_list(self, user: User, category_type: CategoryType | None):
        query = select(Category).where(Category.user_id == user.id)
        if category_type:
            query = query.where(Category.type == category_type)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, id: int, user: User, data: CategoryUpdate) -> Category:
        category = await self._get_by_id(id, user.id)
        if not category:
            raise CategoryNotFound(f"Category with id {id} not found for user {user.email}.")

        update_dict = data.dict() #TODO
        if name := update_dict.get("name"):
            await self._check_existing_category(name, user.id)

        for key, value in update_dict.items():
            setattr(category, key, value)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def _check_existing_category(self, name: str, user_id: UUID) -> None:
        existing_category = await self._get_by_name(name, user_id)
        if existing_category:
            raise CategoryAlreadyExists(existing_category.name)

    async def _get_by_name(self, name: str, user_id: UUID) -> Category | None:
        query = (
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.name == name)
        )
        return await self._get_category(query)

    async def _get_by_id(self, id: int, user_id: UUID) -> Category | None:
        query = (
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.id == id)
        )
        return await self._get_category(query)

    async def _get_category(self, statement: Select) -> Category | None:
        result = await self.session.execute(statement)
        category = result.first()
        if not category:
            return None
        return category[0]


def get_category_repository(session: AsyncSession = Depends(get_async_session)):
    yield CategoryRepository(session)
