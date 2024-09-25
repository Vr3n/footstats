from datetime import datetime
from typing import Any, Dict, List, Tuple, TypedDict
from fastapi import APIRouter, Depends, status
from httpx import AsyncClient, HTTPError, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.logger import logger

from app.models.football import CategoryBase, PublicTournamentWithSeasons, TeamBase, Tournament, TournamentBase, TournamentEvent, TournamentEventBase, TournamentSeasonBase
from app.db.session import get_session

from app.crud.tournament import (tournament_service, category_service,
                                 tournament_season_service, team_service,
                                 tournament_event_service)


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
        raise Exception(f"Tournament Detail scrape error occured: {str(exc)}")


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


class TeamDict(TypedDict):
    name: str
    slug: str
    nameCode: str
    sofascore_id: int


class TournamentEventDict(TypedDict):
    tournament_id: int
    season_id: int
    sofascore_id: int
    homeTeam: TeamDict
    awayTeam: TeamDict
    home_score_current: int | None = None
    home_score_period1: int | None = None
    home_score_period2: int | None = None
    home_score_normaltime: int | None = None

    away_score_current: int | None = None
    away_score_period1: int | None = None
    away_score_period2: int | None = None
    away_score_normaltime: int | None = None

    match_slug: str
    status_code: str
    status_description: str
    status_type: str

    has_xg: str

    startTimestamp: datetime
    endTimestamp: datetime | None = None


def clean_int_from_tuple(data: Tuple[int, ] | int) -> int:
    """
    Cleans up integer from tuple.
    """

    if type(data) is tuple:
        return data[0]
    return data


async def scrape_tournament_events(
        tournament_id: int,
        season_id: int) -> List[TournamentEventDict]:
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

            tmp_data['homeTeam'] = {
                'name': match['homeTeam']['name'],
                'slug': match['homeTeam']['slug'],
                'nameCode': match['homeTeam']['nameCode'],
                'sofascore_id': match['homeTeam']['id'],
            }
            tmp_data['awayTeam'] = {
                'name': match['awayTeam']['name'],
                'slug': match['awayTeam']['slug'],
                'nameCode': match['awayTeam']['nameCode'],
                'sofascore_id': match['awayTeam']['id'],
            }

            home_score_current = clean_int_from_tuple(
                match['homeScore']['current'])

            home_score_period1 = clean_int_from_tuple(
                match['homeScore']['period1'])
            home_score_period2 = clean_int_from_tuple(
                match['homeScore']['period2'])
            home_score_normaltime = clean_int_from_tuple(
                match['homeScore']['normaltime'])

            away_score_current = clean_int_from_tuple(
                match['awayScore']['current'])

            away_score_period1 = clean_int_from_tuple(
                match['awayScore']['period1'])
            away_score_period2 = clean_int_from_tuple(
                match['awayScore']['period2'])
            away_score_normaltime = clean_int_from_tuple(
                match['awayScore']['normaltime'])

            tmp_data['home_score_current'] = home_score_current
            tmp_data['home_score_period1'] = home_score_period1
            tmp_data['home_score_period2'] = home_score_period2
            tmp_data['home_score_normaltime'] = home_score_normaltime

            tmp_data['away_score_current'] = away_score_current
            tmp_data['away_score_period1'] = away_score_period1
            tmp_data['away_score_period2'] = away_score_period2
            tmp_data['away_score_normaltime'] = away_score_normaltime

            tmp_data['match_slug'] = match['slug']

            tmp_data['status_code'] = match['status']['code']
            tmp_data['status_description'] = match['status']['description']
            tmp_data['status_type'] = match['status']['type']

            tmp_data['has_xg'] = match['hasXg']

            tmp_data['startTimestamp'] = datetime.fromtimestamp(
                match['startTimestamp'])
            if 'endTimestamp' in match.keys():
                tmp_data['endTimestamp'] = datetime.fromtimestamp(
                    match['endTimestamp'])
            else:
                tmp_data['endTimestamp'] = None
            match_list.append(tmp_data)

        logger.info(
            f"Tournament Event for tournament {tournament_id} of \
            season {season_id} scraped.")

        print(match_list[0])

        return match_list

    except Exception as exc:
        logger.error(exc)
        raise Exception(f"Tournament event scrape error occured: {str(exc)}")


@router.get(
    "/matches",
    summary="Fetch Matches of the Tournament Season.",
    status_code=status.HTTP_201_CREATED
)
async def scrape_events(
    tournament_id: int,
    season_id: int,
    db: AsyncSession = Depends(get_session)
) -> List[TournamentEvent]:
    event_data = await scrape_tournament_events(
        tournament_id=tournament_id,
        season_id=season_id
    )

    events = list()

    for event in event_data:

        home_team_obj = TeamBase(
            sofascore_id=event['homeTeam']['sofascore_id'],
            slug=event['homeTeam']['slug'],
            name_code=event['homeTeam']['nameCode'],
            name=event['homeTeam']['name']
        )

        away_team_obj = TeamBase(
            sofascore_id=event['awayTeam']['sofascore_id'],
            slug=event['awayTeam']['slug'],
            name_code=event['awayTeam']['nameCode'],
            name=event['awayTeam']['name']
        )

        home_team = await team_service.get_or_create_team(
            db=db, team_data=home_team_obj)
        away_team = await team_service.get_or_create_team(
            db=db, team_data=away_team_obj
        )

        event_obj = TournamentEventBase(
            tournament_id=tournament_id,
            sofascore_id=event['sofascore_id'],
            slug=event['match_slug'],
            home_team_id=home_team.sofascore_id,
            away_team_id=away_team.sofascore_id,
            status_code=event['status_code'],
            status_description=event['status_description'],
            status_type=event['status_type'],
            home_score_current=int(event['home_score_current']),
            home_score_period_1=int(event['home_score_period1']),
            home_score_period_2=int(event['home_score_period2']),
            home_score_normaltime=int(event['home_score_normaltime']),
            home_score_extratime=0,
            home_score_penalties=0,

            away_score_current=int(event['away_score_current']),
            away_score_period_1=int(event['away_score_period1']),
            away_score_period_2=int(event['away_score_period2']),
            away_score_normaltime=int(event['away_score_normaltime']),
            away_score_extratime=0,
            away_score_penalties=0,
            start_timestamp=event['startTimestamp'],
            end_timestamp=event['endTimestamp'],
            has_xg=event['has_xg'],
        )

        event = await tournament_event_service.get_or_create_event(
            db=db,
            event_data=event_obj)

        events.append(event)

    return events


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
            tournament_data['startDateTimestamp']) or None,
        end_timestamp=datetime.fromtimestamp(
            tournament_data['endDateTimestamp']) or None,
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
