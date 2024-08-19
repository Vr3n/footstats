from typing import Dict, Optional
from beanie import WriteRules
from beanie.operators import Or
from logger import logger

from models.documents import Team, Tournament, TournamentEvent, TournamentGroup, TournamentSeason


async def get_tournament(sofascore_id: int, name: str = '') -> Tournament:
    tournament = await Tournament.find_one(
        Or(Tournament.name == name, Tournament.sofascore_id == sofascore_id)
    )
    if not tournament:
        raise Exception("Tournament Does not Exist.")
    return tournament


async def get_tournament_season(sofascore_id: int,
                                year: str = '') -> TournamentSeason:
    tournament = await TournamentSeason.find_one(
        Or(TournamentSeason.sofascore_id == sofascore_id,
           TournamentSeason.year == year)
    )
    if not tournament:
        raise Exception("Tournament Season Does not Exist.")
    return tournament


async def get_or_create_team(data: Dict) -> Team:
    logger.info(f"Received Team: {data}")
    team = await Team.find_one(
        Team.sofascore_id == data['sofascore_id'],
    )

    if not team:
        logger.info(f"Creating Team: {data['name']}")
        team = Team(**data)
        await team.insert()
        logger.info(f"Successfully Created team: {team.name}")
    else:
        logger.info(f"Team already exists: {team.name}")

    return team


async def create_tournament(data: Dict) -> Tournament:
    # Check if tournament already exists.
    logger.info(f"Received data: {data}")

    tournament = await Tournament.find_one(
        {'sofascore_id': data['sofascore_id']}
    )

    if not tournament:
        logger.info(f"Creating Tournament {data['name']}")
        tournament = Tournament(**data)
        await tournament.insert()
        logger.info(f"Sucessfully created tournament: {data['name']}")
    return tournament


async def get_or_create_tournament_seasons(data: Dict,
                                           ) -> TournamentSeason:

    logger.info(f"Received data: {data}")
    season = await TournamentSeason.find_one(
        TournamentSeason.sofascore_id == data['sofascore_id']
    )

    if not season:
        logger.info(f"Creating Season {data}")
        season = TournamentSeason(**data)
        await season.insert()

    return season


async def get_or_create_tournament_groups(
    data: Dict,
) -> TournamentSeason:
    logger.info(f"Received Groups data: {data}")

    group = await TournamentGroup.find_one(
        TournamentGroup.sofascore_id == data['sofascore_id']
    )

    if not group:
        logger.info(f"Creating group {data['name']}")
        group = TournamentGroup(**data)
        await group.insert()
        logger.info(f"Inserted group {group.name} sucessfuly")
    else:
        logger.info(f"Group already exists: {group}")

    return group


async def get_or_create_tournament_events(
    data: Dict,
) -> TournamentEvent:

    logger.info(f"Received event data: {data}")
    event = await Tournament.find_one(
        TournamentEvent.sofascore_id == data['sofascore_id'])

    if not event:
        logger.info(f"Creating Event: {data}")
        event = TournamentEvent(
            **data
        )
        await event.insert()
        logger.info(f"Inserted event {event} sucessfuly")
    else:
        logger.info(f"event already exists: {event}")
    return event
