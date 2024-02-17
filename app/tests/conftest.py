import asyncio

import pytest
import pytest_asyncio
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
async def engine(event_loop):
    engine = create_async_engine(
        settings.ASYNC_POSTGRES_URI,
        echo=False,
        future=True,
    )

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)

    engine.sync_engine.dispose()


@pytest_asyncio.fixture()
async def session(engine):
    SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with SessionLocal(bind=connection) as session:
            nested_transaction = await connection.begin_nested()
            yield session

            if nested_transaction.is_active:
                await nested_transaction.rollback()
            await transaction.rollback()
