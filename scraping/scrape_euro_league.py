import asyncio
from typing import List
import aiohttp
import json
import random
import typing

from datetime import datetime

from beanie import Link, WriteRules

from crud.tournament import create_tournament, get_tournament
from models.documents import TournamentSeason


links = {
    'tournament': 'https://www.sofascore.com/api/v1/unique-tournament/1',
    'tournament_seasons': 'https://www.sofascore.com/api/v1/unique-tournament/1/seasons',
    'tournament_groups': 'https://www.sofascore.com/api/v1/unique-tournament/1/season/56953/groups',
    'tournament_events': 'https://www.sofascore.com/api/v1/tournament/1688/season/56953/events'
}


async def make_request(url: str):
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    user_agent = None

    for _ in range(1, 4):
        user_agent = random.choice(user_agent_list)

    headers = {
        'User-Agent': user_agent
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, ssl=False, headers=headers)

        return response


async def extract_and_store_tournament_details():
    req = await make_request(links['tournament'])

    if req.status == 200:
        print("Request Sent Successfully!")

    data = await req.json()

    print(data)

    data = data['uniqueTournament']

    print("Extracted the data.")

    tournament_data = {
        'name': data['name'],
        'slug': data['slug'],
        'sofascore_id': data['id'],
        'category': {
            'name': data['category']['name'],
            'slug': data['category']['slug'],
            'sofascore_id': data['category']['id'],
        },
        'hasStandingsGroups': data['hasStandingsGroups'],
        'hasGroups': data['hasGroups'],
        'hasPlayoffSeries': data['hasPlayoffSeries'],
        'tournament_start_timestamp': datetime.fromtimestamp(data['startDateTimestamp']),
        'tournament_end_timestamp': datetime.fromtimestamp(data['endDateTimestamp']),
    }

    print(tournament_data, "\n")

    tournament = await create_tournament(tournament_data)

    return tournament


async def extract_and_store_tournament_seasons():
    req = await make_request(links['tournament_seasons'])

    if req.status == 200:
        print("Request Sent Successfully!")

    seasons_data = await req.json()
    seasons_data = seasons_data['seasons']

    tournament = await get_tournament(sofascore_id=1)

    seasons: List[TournamentSeason] = list()
    for season in seasons_data:
        s = TournamentSeason(
            name=season['name'],
            year=season['year'],
            sofascore_id=season['id'],
            tournament=tournament
        )
        seasons.append(s)

    TournamentSeason.insert_many(seasons, link_rule=WriteRules.WRITE)

    return seasons
