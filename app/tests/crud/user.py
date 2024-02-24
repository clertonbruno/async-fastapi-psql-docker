from crud.user import create_user, delete_user, get_user, get_user_by_email, update_user
from fastapi import HTTPException
from models.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7


async def test_create_user(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    assert created_user.id is not None
    assert created_user.email == user.email
    assert created_user.created_at is not None
    assert created_user.updated_at is not None


async def test_create_duplicate_user(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    await create_user(session, user)
    try:
        await create_user(session, user)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.details == "User already exists"


async def test_get_user(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    fetched_user = await get_user(session, create_user.id)
    assert fetched_user == created_user


async def test_get_nonexistent_user(session: AsyncSession):
    fetched_user = await get_user(session, "thisemaildoesntexist@example.com")
    assert fetched_user is None


async def test_get_user_by_email(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    fetched_user = await get_user_by_email(session, user.email)
    assert fetched_user == created_user


async def test_get_nonexisting_user_by_email(session: AsyncSession):
    fetched_user = await get_user_by_email(session, "nonexistent@example.com")
    assert fetched_user is None


async def test_update_user(session: AsyncSession):
    user = UserCreate(
        first_name="John",
        last_name="Doe",
        email="test@example.com",
    )
    created_user = await create_user(session, user)
    updated_user = await update_user(session, user, UserUpdate(first_name="Maverick"))
    assert updated_user.id == created_user.id
    assert updated_user.email == created_user.email
    assert updated_user.first_name != created_user.first_name


async def test_update_nonexistent_user(session: AsyncSession):
    try:
        await update_user(session, uuid7(), UserUpdate(first_name="John"))
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "User not found"


async def test_delete_user(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    deleted_count = await delete_user(session, created_user.id)
    assert deleted_count == 1
    fetched_user = await get_user(session, created_user.id)
    assert fetched_user is None


async def test_delete_nonexistent_user(session: AsyncSession):
    deleted_count = await delete_user(session, uuid7())
    assert deleted_count == 0
