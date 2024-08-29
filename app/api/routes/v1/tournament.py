
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.football import (Tournament, TournamentBase,
                                 TournamentWithCategoryPublic,)
from app.db.session import get_session
from app.crud.tournament import get_all_tournaments


router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all football tournaments.",
    response_model=list[TournamentWithCategoryPublic]
)
async def get_tournaments(*,
                          session: AsyncSession = Depends(get_session)):
    statement = select(Tournament).options(
        selectinload(Tournament.category)
    )

    results = await session.exec(statement)

    tournaments = results.all()

    print(tournaments)

    return tournaments
