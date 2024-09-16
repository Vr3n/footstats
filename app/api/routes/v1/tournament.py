from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.logger import logger

from app.models.football import (Tournament, TournamentBase,
                                 TournamentWithCategoryPublic,)
from app.db.session import get_session
from app.crud.tournament import (tournament_service,)


router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all football tournaments.",
    response_model=List[TournamentWithCategoryPublic]
)
async def get_tournaments(*,
                          category: str | None = None,
                          session: AsyncSession = Depends(get_session),):
    try:
        print(category)
        if category is not None and category != '':
            tournaments = await tournament_service.get_tournaments_by_category(
                session,
                category
            )
        else:
            tournaments = await tournament_service.get_all_tournaments(session)

        return tournaments
    except ResponseValidationError as rve:
        logger.error(f"Get Tournaments: Response error {str(rve)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(rve)
        )
    except Exception as e:
        logger.error(f"Get Tournaments: Unexpected error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))
