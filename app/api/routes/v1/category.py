from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.football import CategoryPublic, PublicCategoryWithTournament
from app.crud.tournament import category_service

from app.logger import logger

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all categories.",
    response_model=List[CategoryPublic]
)
async def get_categories(*,
                         session: AsyncSession = Depends(get_session)):
    try:
        categories = await category_service.get_all_categories(db=session)
        return categories
    except Exception as e:
        logger.error(f"Get Categories: Unexpected error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected Error Occured.")


@router.get(
    "/tournaments",
    status_code=status.HTTP_200_OK,
    summary="All categories with Tournaments",
    response_model=List[PublicCategoryWithTournament]
)
async def get_categories_with_tournaments(*,
                                          session: AsyncSession = Depends(
                                              get_session)):
    try:
        categories = await category_service.get_all_categories(db=session)
        return categories
    except Exception as e:
        logger.error(f"Get Categories: Unexpected error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unexpected Error Occured.")
