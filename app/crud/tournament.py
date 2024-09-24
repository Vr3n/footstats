from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import col, select, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.logger import logger

from app.models.football import (
    Category, CategoryBase, Tournament, TournamentBase,
    TournamentEvent,
    TournamentEventBase,
    TournamentSeason,
    TournamentSeasonBase,
    Team, TournamentGroup,
    TeamBase, TournamentGroupBase,
)
from app.crud.base import CRUDRepository, CRUDRepositoryException


class CategoryService:
    def __init__(self, category_repo: CRUDRepository[Category]):
        self.category_repo: CRUDRepository[Category] = category_repo

    async def get_or_create_category(self, db: AsyncSession,
                                     category_data: CategoryBase) -> Category:
        try:
            category = await self.category_repo.get(db, category_data.sofascore_id)

            if not category:
                obj = Category(
                    sofascore_id=category_data.sofascore_id,
                    name=category_data.name,
                    slug=category_data.slug,
                )
                category = await self.category_repo.create(db, obj)

            return category
        except CRUDRepositoryException as exc:
            logger.error(f"Repository error in CategorySerive: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the category."
            )
        except Exception as exc:
            logger.error(f"Unexpected error in CategoryService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred."
            )

    async def get_all_categories(self,
                                 db: AsyncSession,
                                 ) -> List[Category]:
        try:
            categories = await self.category_repo.get_all(db)
            return categories

        except CRUDRepositoryException as exc:
            logger.error(f"Repository error in CategoryService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching categories."
            )
        except Exception as exc:
            logger.error(f"Unexpected error in CategoryService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred."
            )


class TournamentService:
    def __init__(self,
                 tournament_repo: CRUDRepository[Tournament]):
        self.tournament_repo = tournament_repo

    async def get_or_create_tournament(
            self, db: AsyncSession,
            tournament_data: TournamentBase) -> Tournament:
        try:
            # Try to get the tournament from the repository
            tournament = await self.tournament_repo.get(
                db,
                tournament_data.sofascore_id)
            if not tournament:
                # If tournament not found, create it
                tournament = Tournament(
                    sofascore_id=tournament_data.sofascore_id,
                    name=tournament_data.name,
                    slug=tournament_data.slug,
                    has_rounds=tournament_data.has_rounds,
                    has_groups=tournament_data.has_groups,
                    has_playoff_series=tournament_data.has_playoff_series,
                    start_timestamp=tournament_data.start_timestamp,
                    end_timestamp=tournament_data.end_timestamp,
                    category_id=tournament_data.category_id
                )
                tournament = await self.tournament_repo.create(db, tournament)
            return tournament
        except CRUDRepositoryException as exc:
            logger.error(f"Repository error in TournamentService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the tournament.")
        except Exception as exc:
            logger.error(f"Unexpected error in TournamentService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_tournaments_by_category(self, db: AsyncSession,
                                          category: str) -> List[Tournament]:
        try:
            if isinstance(category, int) or category.isdigit():
                category = int(category)
                query = select(Tournament).join(
                    Category, Tournament.category_id == Category.sofascore_id
                ).where(
                    Category.sofascore_id == category
                )
            else:
                query = select(Category).join(
                    Category, Tournament.category_id == Category.sofascore_id
                ).where(
                    Category.name == category
                )
            tournaments = await db.exec(query)

            return tournaments
        except CRUDRepositoryException as exc:
            logger.error(f"Repository Error in TournamentService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured while fetching tournament by category."
            )

    async def get_tournaments_by_name(
            self, db: AsyncSession,
            tournament_name: str) -> List[Tournament] | Tournament:
        try:
            query = select(Tournament).where(
                col(Tournament.name).icontains(tournament_name))

            tournaments = await db.exec(query)

            return tournaments
        except CRUDRepositoryException as exc:
            logger.error(f"Tournament Name: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured while fetching tournament by name."
            )

    async def get_all_tournaments(self, db: AsyncSession) -> List[Tournament]:
        try:
            tournaments = await self.tournament_repo.get_all(db=db)
            return tournaments
        except CRUDRepositoryException as exc:
            logger.error(f"Repository error in TournamentService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching tournaments.")
        except Exception as exc:
            logger.error(f"Unexpected error in TournamentService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")


class TournamentEventService:
    def __init__(self, event_repo: CRUDRepository[TournamentEvent]):
        self.event_repo = event_repo

    async def create_tournament_event(self, db: AsyncSession, event_data: TournamentEventBase) -> TournamentEvent:
        try:
            # Create a new tournament event
            event = TournamentEvent(
                sofascore_id=event_data.sofascore_id,
                slug=event_data.slug,
                detail_id=event_data.detail_id,
                stage_id=event_data.stage_id,
                tournament_id=event_data.tournament_id,
                home_team_id=event_data.home_team_id,
                away_team_id=event_data.away_team_id,
                home_score_period_1=event_data.home_score_period_1,
                home_score_period_2=event_data.home_score_period_2,
                home_score_normaltime=event_data.home_score_normaltime,
                home_score_extratime=event_data.home_score_extratime,
                home_score_penalties=event_data.home_score_penalties,
                away_score_period_1=event_data.away_score_period_1,
                away_score_period_2=event_data.away_score_period_2,
                away_score_normaltime=event_data.away_score_normaltime,
                away_score_extratime=event_data.away_score_extratime,
                away_score_penalties=event_data.away_score_penalties,
                has_xg=event_data.has_xg,
                has_eventplayer_statistics=event_data.has_eventplayer_statistics,
                has_eventplayer_heatmap=event_data.has_eventplayer_heatmap
            )
            event = await self.event_repo.create(db, event)
            return event
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentEventService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the tournament event.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentEventService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_event_by_id(self, db: AsyncSession, event_id: int) -> TournamentEvent:
        try:
            event = await self.event_repo.get(db, event_id)
            return event
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentEventService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching the event.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentEventService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_all_events(self, db: AsyncSession) -> List[TournamentEvent]:
        try:
            events = await self.tournament_event_repo.get_all(db)
            if not events:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No tournament events found.")
            return events
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentEventService - get_all_events: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while fetching tournament events.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentEventService - get_all_events: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def update_event(self, db: AsyncSession, event_id: int, event_data: TournamentEventBase) -> TournamentEvent:
        try:
            event = await self.tournament_event_repo.get(db, event_id)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tournament event not found.")

            # Update event attributes
            event.slug = event_data.slug or event.slug
            event.detail_id = event_data.detail_id or event.detail_id
            event.home_team_id = event_data.home_team_id or event.home_team_id
            event.away_team_id = event_data.away_team_id or event.away_team_id
            event.home_score_period_1 = event_data.home_score_period_1 or event.home_score_period_1
            event.away_score_period_1 = event_data.away_score_period_1 or event.away_score_period_1
            event.home_score_period_2 = event_data.home_score_period_2 or event.home_score_period_2
            event.away_score_period_2 = event_data.away_score_period_2 or event.away_score_period_2
            event.home_score_normaltime = event_data.home_score_normaltime or event.home_score_normaltime
            event.away_score_normaltime = event_data.away_score_normaltime or event.away_score_normaltime
            event.home_score_extratime = event_data.home_score_extratime or event.home_score_extratime
            event.away_score_extratime = event_data.away_score_extratime or event.away_score_extratime
            event.home_score_penalties = event_data.home_score_penalties or event.home_score_penalties
            event.away_score_penalties = event_data.away_score_penalties or event.away_score_penalties
            event.has_xg = event_data.has_xg
            event.has_eventplayer_statistics = event_data.has_eventplayer_statistics or event.has_eventplayer_statistics
            event.has_eventplayer_heatmap = event_data.has_eventplayer_heatmap

            updated_event = await self.tournament_event_repo.update(db, event)
            return updated_event
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentEventService - update_event: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while updating the tournament event.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentEventService - update_event: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def delete_event(self, db: AsyncSession, event_id: int) -> None:
        try:
            event = await self.tournament_event_repo.get(db, event_id)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tournament event not found.")

            await self.tournament_event_repo.delete(db, event)
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentEventService - delete_event: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while deleting the tournament event.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentEventService - delete_event: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")


class TournamentSeasonService:
    def __init__(self, tournament_season_repo: CRUDRepository[TournamentSeason]):
        self.tournament_season_repo = tournament_season_repo

    async def create_tournament_season(self,
                                       db: AsyncSession,
                                       season_data: TournamentSeasonBase
                                       ) -> TournamentSeason:
        try:
            # Create a new tournament season
            tournament_season = TournamentSeason(
                sofascore_id=season_data.sofascore_id,
                name=season_data.name,
                year=season_data.year,
                tournament_id=season_data.tournament_id
            )
            created_season = await self.tournament_season_repo.create(db, tournament_season)
            return created_season
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while creating the tournament season.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_tournament_season_by_id(self, db: AsyncSession, season_id: int) -> TournamentSeason:
        try:
            season = await self.tournament_season_repo.get(db, season_id)
            if not season:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Tournament season not found.")
            return season
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while fetching the tournament season.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_all_tournament_seasons(
            self, db: AsyncSession) -> List[TournamentSeason]:
        try:
            seasons = await self.tournament_season_repo.get_all(db)
            return seasons
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while fetching tournament seasons.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def update_tournament_season(self, db: AsyncSession, season_id: int, season_data: TournamentSeasonBase) -> TournamentSeason:
        try:
            season = await self.tournament_season_repo.get(db, season_id)
            if not season:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tournament season not found.")

            # Update season attributes
            season.name = season_data.name
            season.year = season_data.year
            season.tournament_id = season_data.tournament_id

            updated_season = await self.tournament_season_repo.update(db, season)
            return updated_season
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while updating the tournament season.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def delete_tournament_season(self, db: AsyncSession, season_id: int) -> None:
        try:
            season = await self.tournament_season_repo.get(db, season_id)
            if not season:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tournament season not found.")

            await self.tournament_season_repo.delete(db, season)
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while deleting the tournament season.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentSeasonService: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred.")

    async def get_or_create_season(self, db: AsyncSession,
                                   season_data: TournamentSeasonBase
                                   ) -> TournamentSeason:
        try:
            season = await self.tournament_season_repo.get(
                db,
                season_data.sofascore_id)

            if not season:
                season = TournamentSeason(
                    sofascore_id=season_data.sofascore_id,
                    name=season_data.name,
                    year=season_data.year,
                    tournament_id=season_data.tournament_id
                )

                season = await self.tournament_season_repo.create(db, season)

            return season
        except CRUDRepositoryException as exc:
            logger.error(f"Repository error in Get Create Season: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the season."
            )
        except Exception as exc:
            logger.error(f"Unexpected error in Season service: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred."
            )


class TeamService:
    def __init__(self, team_repo: CRUDRepository[Team]):
        self.team_repo = team_repo

    # Basic CRUD functions

    async def create_team(self, db: AsyncSession, team_data: TeamBase) -> Team:
        try:
            new_team = await self.team_repo.create(db, team_data)
            return new_team
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TeamService - create_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating team.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - create_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def get_team_by_id(self, db: AsyncSession, team_id: int) -> Team:
        try:
            team = await self.team_repo.get(db, team_id)
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
            return team
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TeamService - get_team_by_id: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching team.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - get_team_by_id: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def update_team(self, db: AsyncSession, team_id: int, team_data: TeamBase) -> Team:
        try:
            team = await self.team_repo.get(db, team_id)
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

            updated_team = await self.team_repo.update(db, team)
            return updated_team
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TeamService - update_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating team.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - update_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def delete_team(self, db: AsyncSession, team_id: int) -> None:
        try:
            team = await self.team_repo.get(db, team_id)
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

            await self.team_repo.delete(db, team)
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TeamService - delete_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting team.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - delete_team: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    # Extra Functions

    async def get_team_by_tournament(self, db: AsyncSession, tournament_id: int, season_id: int) -> List[Team]:
        try:
            query = select(Team).join(TournamentEvent).where(
                TournamentEvent.tournament_id == tournament_id,
                TournamentEvent.season_id == season_id
            )
            result = await db.exec(query)
            teams = result.scalars().all()
            if not teams:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No teams found for the given tournament and season.")
            return teams
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - get_team_by_tournament: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def get_team_by_tournament_group(self, db: AsyncSession, group_id: int, season_id: int) -> List[Team]:
        try:
            query = select(Team).join(TournamentEvent).where(
                TournamentEvent.stage_id == group_id,
                TournamentEvent.season_id == season_id
            )
            result = await db.exec(query)
            teams = result.scalars().all()
            if not teams:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No teams found for the given tournament group and season.")
            return teams
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - get_team_by_tournament_group: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def get_team_by_season(self, db: AsyncSession, season_id: int) -> List[Team]:
        try:
            query = select(Team).join(TournamentEvent).where(
                TournamentEvent.season_id == season_id
            )
            result = await db.exec(query)
            teams = result.scalars().all()
            if not teams:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No teams found for the given season.")
            return teams
        except Exception as exc:
            logger.error(
                f"Unexpected error in TeamService - get_team_by_season: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")


class TournamentGroupService:
    def __init__(self, tournament_group_repo: CRUDRepository[TournamentGroup]):
        self.tournament_group_repo = tournament_group_repo

    # Basic CRUD functions

    async def create_group(self, db: AsyncSession, group_data: TournamentGroupBase) -> TournamentGroup:
        try:
            new_group = await self.tournament_group_repo.create(db, group_data)
            return new_group
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentGroupService - create_group: {str(exc)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error creating tournament group.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentGroupService - create_group: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def get_group_by_id(self, db: AsyncSession, group_id: int) -> TournamentGroup:
        try:
            group = await self.tournament_group_repo.get(db, group_id)
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Tournament group not found.")
            return group
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentGroupService - get_group_by_id: {str(exc)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error fetching tournament group.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentGroupService - get_group_by_id: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def update_group(self, db: AsyncSession, group_id: int, group_data: TournamentGroupBase) -> TournamentGroup:
        try:
            group = await self.tournament_group_repo.get(db, group_id)
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Tournament group not found.")

            updated_group = await self.tournament_group_repo.update(db, group)
            return updated_group
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentGroupService - update_group: {str(exc)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error updating tournament group.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentGroupService - update_group: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    async def delete_group(self, db: AsyncSession, group_id: int) -> None:
        try:
            group = await self.tournament_group_repo.get(db, group_id)
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Tournament group not found.")

            await self.tournament_group_repo.delete(db, group)
        except CRUDRepositoryException as exc:
            logger.error(
                f"Repository error in TournamentGroupService - delete_group: {str(exc)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error deleting tournament group.")
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentGroupService - delete_group: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")

    # Extra Function

    async def get_group_by_season(self, db: AsyncSession, season_id: int) -> List[TournamentGroup]:
        try:
            query = select(TournamentGroup).where(
                TournamentGroup.tournament_season_id == season_id)
            result = await db.exec(query)
            groups = result.scalars().all()
            if not groups:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No tournament groups found for the given season.")
            return groups
        except Exception as exc:
            logger.error(
                f"Unexpected error in TournamentGroupService - get_group_by_season: {str(exc)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred.")


tournament_service = TournamentService(
    tournament_repo=CRUDRepository(model=Tournament))
category_service = CategoryService(
    category_repo=CRUDRepository(model=Category))
tournament_season_service = TournamentSeasonService(
    tournament_season_repo=CRUDRepository(model=TournamentSeason)
)
tournament_event_service = TournamentEventService(
    event_repo=CRUDRepository(model=TournamentEvent)
)
