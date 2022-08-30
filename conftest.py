import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.users.api import current_user
from core.users.models import User
from settings.db import async_session_maker, Base, engine
from main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    async with async_session_maker() as async_session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield async_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    create_dict = {"email": "abc@mail.com", "hashed_password": "secret"}
    instance = User(**create_dict)
    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@pytest_asyncio.fixture
async def as_anonymous():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest_asyncio.fixture
async def as_user(user):
    app.dependency_overrides[current_user] = lambda: user
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client
