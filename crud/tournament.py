from typing import Dict
from beanie.operators import Or

from models.documents import Tournament, TournamentSeason


async def get_tournament(sofascore_id: int, name: str = '') -> Tournament:
    tournament = await Tournament.find_one(
        Or(Tournament.name == name, Tournament.sofascore_id == sofascore_id)
    )
    if not tournament:
        raise Exception("Tournament Does not Exist.")
    return tournament


async def create_tournament(data: Dict) -> Tournament:
    # Check if tournament already exists.
    print("got the data: ", data)
    tournament = await Tournament.find_one(
        {'sofascore_id': data['sofascore_id']}
    )

    if not tournament:
        tournament = Tournament(
            name=data['name'],
            slug=data['slug'],
            sofascore_id=data['sofascore_id'],
            has_standings_groups=data['hasStandingsGroups'],
            has_groups=data['hasGroups'],
            has_playoff_series=data['hasPlayoffSeries'],
            start_timestamp=data['tournament_start_timestamp'],
            end_timestamp=data['tournament_end_timestamp'],
            category=data['category']
        )
        await tournament.insert()
    return tournament


async def get_or_create_tournament_seasons(data: Dict,
                                           tournament: Tournament) -> TournamentSeason:
    season = TournamentSeason.find_one(sofascore_id=data['sofascore_id'])

    if not season:
        season = TournamentSeason(
            sofascore_id=data['sofascore_id'],
            name=data['name'],
            year=data['year'],
            tournament=Tournament(tournament)
        )
        await season.insert()

    return season
