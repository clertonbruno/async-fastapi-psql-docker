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
