import asyncio
from typing import Any, Dict, List
from datetime import datetime

from beanie import WriteRules
from httpx import AsyncClient, Response
import httpx
from logger import logger

from crud.tournament import create_tournament, get_or_create_team, get_or_create_tournament_events, get_or_create_tournament_groups, get_or_create_tournament_seasons
from models.documents import TeamScores, Tournament, TournamentEvent, TournamentGroup, TournamentSeason


temp_links = {
    'tournament': 'https://www.sofascore.com/api/v1/unique-tournament/1',
    'tournament_seasons': 'https://www.sofascore.com/api/v1/unique-tournament/1/seasons',
    'tournament_groups': 'https://www.sofascore.com/api/v1/unique-tournament/1/season/56953/groups',
    'tournament_events': 'https://www.sofascore.com/api/v1/tournament/1688/season/56953/events'
}


# SofaScore API endpoints
links = {
    'tournament': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}',
    'tournament_seasons': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons',
    'tournament_groups': 'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/groups',
    'tournament_events': 'https://www.sofascore.com/api/v1/tournament/{tournament_id}/season/{season_id}/events'
}


class Euro2024Scraper:

    def __init__(self, tournament_id: int) -> None:
        self.tournament_id = tournament_id

    async def fetch_data(self, client_url: str) -> Response:
        async with AsyncClient() as client:
            try:
                res = await client.get(client_url)
                res.raise_for_status()
                return res
            except httpx.HTTPError as exc:
                logger.error(f"HTTP exception for {exc.request.url} - {exc}")

    def get_json_data(self, res: Response) -> Dict[str, Any]:
        data = res.json()

        if data is None:
            logger.error("No data returned")
            raise Exception("No data returned")

        return data

    async def scrape_tournament_details(self,
                                        tournament_id: int) -> Tournament:
        url = links['tournament'].format(tournament_id=tournament_id)

        res = await self.fetch_data(url)

        try:
            data = self.get_json_data(res)
            logger.info("Received data")

            data = data['uniqueTournament']

            tournament_data = {
                'name': data['name'],
                'slug': data['slug'],
                'sofascore_id': data['id'],
                'category': {
                    'name': data['category']['name'],
                    'slug': data['category']['slug'],
                    'sofascore_id': data['category']['id'],
                },
                'has_standings_groups': data['hasStandingsGroups'],
                'has_groups': data['hasGroups'],
                'has_playoff_series': data['hasPlayoffSeries'],
                'has_rounds': data['hasRounds'],
                'start_timestamp': datetime.fromtimestamp(
                    data['startDateTimestamp']),
                'end_timestamp': datetime.fromtimestamp(
                    data['endDateTimestamp']),
            }

            tournament = await create_tournament(tournament_data)

            logger.info("Completed Scraping the tournament.")

            return tournament
        except Exception as exc:
            logger.error(exc)

    async def scrape_tournament_seasons(
            self, tournament: Tournament) -> List[TournamentSeason]:
        url = links['tournament_seasons'].format(
            tournament_id=tournament.sofascore_id)

        res = await self.fetch_data(url)

        try:
            data = self.get_json_data(res)
            logger.info("Received data")

            seasons_data = data['seasons']
            logger.info(seasons_data)

            seasons: List[TournamentSeason] = list()
            for season in seasons_data:
                tmp_data = {
                    "name": season['name'],
                    "year": season['year'],
                    "sofascore_id": season['id'],
                    "tournament": tournament
                }

                s = await get_or_create_tournament_seasons(tmp_data)
                seasons.append(s)

            return seasons
        except Exception as exc:
            logger.error(exc)

    async def scrape_tournament_groups(self,
                                       tournament: Tournament,
                                       season: TournamentSeason,
                                       ) -> List[TournamentGroup]:
        url = links['tournament_groups'].format(
            tournament_id=tournament.sofascore_id,
            season_id=season.sofascore_id
        )

        res = await self.fetch_data(url)

        try:
            data = self.get_json_data(res)
            logger.info(f"received group: {data}")
            groups = []

            group_list = [
                {"sofascore_id": d['tournamentId'],
                 "name": d['groupName'],
                 "season": season,
                 "tournament": tournament
                 } for d in data['groups']
            ]

            for group in group_list:
                g = await get_or_create_tournament_groups(group)
                groups.append(g)

            asyncio.sleep(5)

            return groups
        except TypeError:
            logger.error("Type error")
        except Exception as exc:
            logger.error(exc)

    async def scrape_tournament_events(self,
                                       tournament: Tournament,
                                       group: TournamentGroup,
                                       ) -> List[TournamentEvent]:
        await group.fetch_link(TournamentGroup.season)

        url = links['tournament_events'].format(
            tournament_id=group.sofascore_id,
            season_id=group.season.sofascore_id)

        res = await self.fetch_data(url)

        try:
            data = self.get_json_data(res)

            tournament_events = data['events']

            # logger.info(f"Received event data: {tournament_events}")

            tournament_matches = []

            for match in tournament_events:

                home_team = await get_or_create_team({
                    'sofascore_id': match['homeTeam']['id'],
                    'slug': match['homeTeam']['slug'],
                    'name_code': match['homeTeam']['nameCode'],
                    'ranking': match['homeTeam']['ranking'],
                    'name': match['homeTeam']['name']
                })
                away_team = await get_or_create_team({
                    'sofascore_id': match['awayTeam']['id'],
                    'slug': match['awayTeam']['slug'],
                    'name_code': match['awayTeam']['nameCode'],
                    'ranking': match['awayTeam']['ranking'],
                    'name': match['awayTeam']['name']
                })

                match_data = {
                    "sofascore_id": match['id'],
                    "stage": group,
                    "tournament": tournament,
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": TeamScores(**match['homeScore']),
                    "away_score": TeamScores(**match['awayScore']),
                    "has_xg": match['hasXg'],
                    "has_eventplayer_statistics": match[
                        'hasEventPlayerStatistics'],
                    "has_eventplayer_heatmap": match[
                        'hasEventPlayerHeatMap'],
                    "slug": match['slug'],
                    "detail_id": match['detailId']
                }

                tournament_event = await get_or_create_tournament_events(
                    match_data
                )

                tournament_matches.append(tournament_event)

                asyncio.sleep(5)

            return tournament_matches
        except TypeError as type_err:
            logger.error("Type error", type_err)
        except Exception as exc:
            logger.error(exc)

    async def run_scraper(self):
        tournament = await self.scrape_tournament_details(
            tournament_id=self.tournament_id)

        asyncio.sleep(5)

        seasons = await self.scrape_tournament_seasons(
            tournament=tournament
        )

        groups_scrape_tasks: List[TournamentGroup] = []
        for season in seasons:
            groups_scrape_tasks.append(
                self.scrape_tournament_groups(tournament=tournament,
                                              season=season)
            )
        await asyncio.gather(*groups_scrape_tasks)

        events_scrape_tasks = list()
        groups = await TournamentGroup.find_all().to_list()
        for group in groups:
            events_scrape_tasks.append(
                self.scrape_tournament_events(
                    tournament=tournament,
                    group=group
                )
            )
        await asyncio.gather(*events_scrape_tasks)


euro_scraper = Euro2024Scraper(tournament_id=1)
