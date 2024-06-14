from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional
from beanie import Document, Link


class Category(BaseModel):
    sofascore_id: Optional[int]
    name: str
    slug: Optional[str]


class Tournament(Document):
    sofascore_id: int
    category: Optional[Category]
    name: str
    slug: Optional[str]
    has_standings_groups: bool = False
    has_groups: bool = False
    has_rounds: bool = False
    has_playoff_series: bool = False
    sofascore_link: Optional[str] = ''

    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]

    class Settings:
        name = "tournaments"


class TournamentSeason(Document):
    sofascore_id: int
    tournament: Link[Tournament]
    name: str
    year: str

    class Settings:
        name = "tournamentseasons"


class TournamentGroup(Document):
    sofascore_id: int
    tournament_season: Link[TournamentSeason]
    name: str

    class Settings:
        name = "tournamentgroups"


class Team(Document):
    sofascore_id: int
    name: str
    name_code: str
    country: Optional[str]
    slug: str

    class Settings:
        name = "teams"


class TeamScores(BaseModel):
    period1: int = 0
    period2: int = 0
    normalTime: int = 0
    extraTime: int = 0
    penalties: int = 0


class TournamentEvent(Document):
    sofascore_id: int
    stage: Optional[Link[TournamentGroup]]
    tournament: Link[Tournament]
    tournament_season: Optional[Link[TournamentSeason]]
    home_team: Link[Team]
    away_team: Link[Team]
    home_score: TeamScores
    away_score: TeamScores

    class Settings:
        name = "tournamentevents"


BEANIE_MODELS = [
    Tournament,
    TournamentSeason,
    TournamentGroup,
    Team,
    TournamentEvent
]
