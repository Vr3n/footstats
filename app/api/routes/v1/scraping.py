from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, status
from httpx import AsyncClient, HTTPError, Response

from app.logger import logger

from app.models.football import CategoryBase, Tournament, TournamentBase
from app.crud.tournament import get_or_create_category, get_or_create_tournament
from app.crud.tournament import get_or_create_tournament_seasons


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
            tmp_data['sofascore_id'] = season['sofascore_id']
            tmp_data['tournament_id'] = tournament_id
            seasons.append(tmp_data)

        return seasons

    except Exception as exc:
        logger.error(exc)


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
        logger.error(exc)


@router.get(
    "/tournaments",
    summary="scrape tournaments",
    status_code=status.HTTP_201_CREATED,
)
async def scrape_tournament(tournament_id: int) -> TournamentBase:
    tournament_data = await scrape_tournament_details(
        tournament_id=tournament_id)

    category_data = CategoryBase(
        sofascore_id=tournament_data['category']['id'],
        name=tournament_data['category']['name'],
        slug=tournament_data['category']['slug']
    )

    category = await get_or_create_category(category_data)

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

    tournament = await get_or_create_tournament(tournament_data)

    # seasons_data = await scrape_tournament_seasons(tournament_id=tournament_id)
    #
    # seasons = list()
    # for season in seasons_data:
    #     tmp_seas = await get_or_create_tournament_seasons(
    #         season
    #     )
    #     seasons.append(tmp_seas)
    #
    # print(seasons)

    return tournament
