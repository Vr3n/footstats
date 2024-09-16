from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from httpx import AsyncClient, HTTPError, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.logger import logger

from app.models.football import CategoryBase, PublicTournamentWithSeasons, Tournament, TournamentBase, TournamentSeasonBase
from app.db.session import get_session

from app.crud.tournament import (tournament_service, category_service,
                                 tournament_season_service,)


router = APIRouter(prefix='/scrape', tags=['scraper'])

#
links = {
    'tournament': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}',
    'tournament_seasons': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons',
    'tournament_season_statistics': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/statistics?limit={limit}&offset={offset}&order=-rating&accumulation={acc}&group={grp}',
    'tournament_events': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/team-events/total',
    'team_performance_data': 'https://www.sofascore.com/api/v1/unique-tournament/17/season/52186/team/42/team-performance-graph-data',
    'event_statistic': 'https://www.sofascore.com/api/v1/event/{event_id}/statistics',
    'event_shotmaps': 'https://www.sofascore.com/api/v1/event/{event_id}/shotmap',
    'event_lineups': 'https://www.sofascore.com/api/v1/event/{event_id}/lineups',
}


async def fetch_data(client_url: str) -> Response:
    async with AsyncClient() as client:
        try:
            logger.info(f"fetching data for {client_url}")
            res = await client.get(client_url)
            res.raise_for_status()
            return res
        except HTTPError as exc:
            logger.error(f"HTTP exception for {exc.request.url} - {exc}")


def get_json_data(res: Response) -> Dict[str, Any]:
    data = res.json()

    if data is None:
        logger.error("No data returned")
        raise Exception("No data returned")
    return data


async def scrape_tournament_details(tournament_id: int) -> Dict[str, Any]:
    url = links['tournament'].format(tournament_id=tournament_id)

    res = await fetch_data(url)

    try:
        data = get_json_data(res)
        data = data['uniqueTournament']
        logger.info(f"Received Data for tournament - {tournament_id}")
        return data

    except Exception as exc:
        logger.error(exc)


async def scrape_tournament_seasons(tournament_id: int) -> Dict[str, Any]:
    url = links['tournament_seasons'].format(
        tournament_id=tournament_id
    )

    res = await fetch_data(url)

    try:
        data = get_json_data(res)
        data = data['seasons']

        seasons = list()
        for season in data:
            tmp_data = dict()
            tmp_data['name'] = season['name']
            tmp_data['year'] = season['year']
            tmp_data['sofascore_id'] = season['id']
            tmp_data['tournament_id'] = tournament_id
            seasons.append(tmp_data)

        return seasons

    except Exception as exc:
        logger.error(exc)
        raise Exception(f"An unexpected error occured: {str(exc)}")


async def scrape_tournament_events(tournament_id: int,
                                   season_id: int) -> Dict[str, Any]:
    url = links['tournament_events'].format(
        tournament_id=tournament_id,
        season_id=season_id,
    )

    res = await fetch_data(url)

    try:
        data = get_json_data(res)
        data = data['tournamentTeamEvents']['1'].values()
        match_data = [
            match for matchweek in data for match in matchweek
        ]
        match_list = list()

        for match in match_data:
            tmp_data = {}
            tmp_data['tournament_id'] = tournament_id
            tmp_data['season_id'] = season_id
            tmp_data['sofascore_id'] = match['id']

        return match_list

    except Exception as exc:
        logger.error(f"Tournament Events Scrape: {str(exc)}")
        raise Exception("An unexpected error occured")


@router.get(
    "/tournaments",
    summary="scrape tournaments",
    status_code=status.HTTP_201_CREATED,
)
async def scrape_tournament(tournament_id: int,
                            db: AsyncSession = Depends(get_session)
                            ) -> PublicTournamentWithSeasons:
    tournament_data = await scrape_tournament_details(
        tournament_id=tournament_id)

    category_data = CategoryBase(
        sofascore_id=tournament_data['category']['id'],
        name=tournament_data['category']['name'],
        slug=tournament_data['category']['slug']
    )

    category = await category_service.get_or_create_category(db, category_data)

    tournament_data = TournamentBase(
        sofascore_id=tournament_data['id'],
        name=tournament_data['name'],
        slug=tournament_data['slug'],
        has_rounds=tournament_data['hasRounds'],
        has_groups=tournament_data['hasGroups'],
        has_playoff_series=tournament_data['hasPlayoffSeries'],
        start_timestamp=datetime.fromtimestamp(
            tournament_data['startDateTimestamp']),
        end_timestamp=datetime.fromtimestamp(
            tournament_data['endDateTimestamp']),
        category_id=category.sofascore_id,
    )

    tournament = await tournament_service.get_or_create_tournament(
        db,
        tournament_data
    )

    seasons_data = await scrape_tournament_seasons(tournament_id=tournament_id)

    for season in seasons_data:
        season_obj = TournamentSeasonBase(
            sofascore_id=season['sofascore_id'],
            year=season['year'],
            tournament_id=season['tournament_id'],
            name=season['name'],
        )
        _ = await tournament_season_service.get_or_create_season(
            db,
            season_obj
        )

    await db.refresh(tournament)

    return tournament
