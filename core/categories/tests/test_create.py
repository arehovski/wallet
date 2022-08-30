import pytest
from httpx import AsyncClient
from sqlalchemy import select

from core.categories.models import CategoryType, Category
from core.categories.schemas import CategoryCreate


@pytest.fixture
def url_create():
    return "/categories/"


@pytest.mark.asyncio
async def test_is_forbidden_for_non_authenticated(as_anonymous: AsyncClient, url_create):
    response = await as_anonymous.post(
        url_create, data=CategoryCreate(name="abc", starting_balance=0, type=CategoryType.ACCOUNT).dict()
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_category_is_created(as_user: AsyncClient, user, url_create):
    response = await as_user.post(
        url_create, data=CategoryCreate(name="abc", starting_balance=0, type=CategoryType.ACCOUNT).dict()
    )

    assert response.status_code == 201
    category = select(Category).where(Category.user_id == user.id)
    assert category.name == "abc"
    assert category.starting_balance == 0
