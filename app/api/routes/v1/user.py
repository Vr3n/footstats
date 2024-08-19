
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import create_user
from app.db.session import get_session
from app.models.user import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user_route(
    data: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_user(session=db, user=data)
