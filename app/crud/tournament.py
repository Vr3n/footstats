from typing import Any, Dict, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.logger import logger

from app.models.football import (
    Category, CategoryBase, Tournament, TournamentBase)
from app.db.session import engine
from app.models.football import (
    TournamentEvent,
    TournamentEventBase,
    TournamentSeason,
    TournamentSeasonBase,
)


async def get_or_create_category(category_data: CategoryBase) -> Category:
    async with AsyncSession(engine) as session:
        category_select = select(Category).where(
            Category.sofascore_id == category_data.sofascore_id)

        results = await session.exec(category_select)
        category = results.first()

        if not category:
            logger.info("Category not found, creating new category")
            category = Category.model_validate(category_data)

            session.add(category)
            await session.commit()
            logger.info(f"Category {category.name} created successfully!")
        else:
            logger.info(f"Found Category {category}")

    return category


async def get_or_create_tournament(
        tournament_data: TournamentBase) -> Tournament:
    async with AsyncSession(engine) as session:
        tournament_select = select(Tournament).where(
            Tournament.sofascore_id == tournament_data.sofascore_id
        )

        results = await session.exec(tournament_select)
        tournament = results.first()

        if not tournament:
            logger.info("Tournament not found, creating new tournament")
            tournament = Tournament.model_validate(tournament_data)

            session.add(tournament)
            await session.commit()
            logger.info(f"Tournament {tournament.name} created successfully!")
        else:
            logger.info(f"Found tournament {tournament.name}")

    return tournament


async def get_or_create_tournament_seasons(
    seasons_data: TournamentSeasonBase
) -> TournamentSeason:
    async with AsyncSession(engine) as session:
        season_select = select(TournamentSeason).where(
            TournamentSeason.sofascore_id == seasons_data.sofascore_id
        )

        results = await session.exec(season_select)
        season = results.first()

        if not season:
            logger.info("Season not found, creating new season")
            season = TournamentSeason.model_validate(seasons_data)

            session.add(season)
            await session.commit()
            logger.info(f"Season {season.name} created successfully!")
        else:
            logger.info(f"Found season {season.name}")

    return season


async def get_or_create_tournament_events(
    events_data: TournamentEventBase
) -> TournamentEvent:
    async with AsyncSession(engine) as session:
        event_select = select(TournamentEvent).where(
            TournamentEvent.sofascore_id == events_data.sofascore_id
        )

        results = await session.exec(event_select)
        event = results.first()

        if not event:
            logger.info("Event not found, creating new Event")
            event = TournamentEvent.model_validate(events_data)

            session.add(event)
            await session.commit()
            logger.info(f"Event {event.name} created successfully!")
        else:
            logger.info(f"Found event {event.name}")

    return event


async def create_tournament_events(
        event_data: TournamentEventBase) -> TournamentEvent:
    async with AsyncSession(engine) as session:
        logger.info("Creating new Event")
        event = TournamentEvent.model_validate(event_data)

        session.add(event)
        await session.commit()
        logger.info(f"Event {event.name} created successfully!")
    return event
