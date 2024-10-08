from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7
from app.models.user import User, UserCreate, UserUpdate
from app.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    update_user,
    delete_user,
)


async def test_create_user(session: AsyncSession):
    user: UserCreate = UserCreate(email="text@example.com")
    created_user = await create_user(session, user)
    assert created_user.id is not None
    assert created_user.email == user.email
    assert create_user.created_at is not None
    assert create_user.updated_at is not None


async def test_create_duplicate_user(session: AsyncSession):
    user: UserCreate = UserCreate(email="test@example.com")
    await create_user(session, user)
    try:
        await create_user(session, user)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == "User already exists"


async def test_get_user(session: AsyncSession):
    user: UserCreate = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    retrieved_user = await get_user(session, created_user.id)
    assert retrieved_user == created_user


async def test_get_nonexistent_user(session: AsyncSession):
    retrieved_user = await get_user(session, uuid7())
    assert retrieved_user is None


async def test_get_user_by_email(session: AsyncSession):
    user = UserCreate(email="test@example.com")
    created_user = await create_user(session, user)
    retrieved_user = await get_user_by_email(session, user.email)
    assert retrieved_user == created_user


async def test_get_nonexistent_user_by_email(session: AsyncSession):
    retrieved_user = await get_user_by_email(session,
                                             "nonexistent@example.com")
    assert retrieved_user is None


async def test_update_user(session: AsyncSession):
    created_user: User = await create_user(
        session, UserCreate(first_name="alice", email="test@example.com")
    )
    updated_user: User = await update_user(
        session, created_user.id, UserUpdate(first_name="bob")
    )
    assert updated_user.id == created_user.id
    assert updated_user.email == created_user.email
    assert updated_user.first_name == "bob"


async def test_update_nonexistent_user(session: AsyncSession):
    try:
        await update_user(session, uuid7(), UserUpdate(first_name="alice"))
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "User not found."


async def test_delete_user(session: AsyncSession):
    created_user: User = await create_user(session,
                                           UserCreate(email="test@example.com")
                                           )
    deleted_count = await delete_user(session, created_user.id)
    assert deleted_count == 1
    retrieved_user = await get_user(session, created_user.id)
    assert retrieved_user is None


async def test_delete_nonexistent_user(session: AsyncSession):
    deleted_count = await delete_user(session, uuid7())
    assert deleted_count == 0
