from datetime import datetime
from pydantic import BaseModel
from typing import Annotated, Optional
from beanie import Document, Indexed, Link, PydanticObjectId


class Category(BaseModel):
    sofascore_id: Optional[int]
    name: str
    slug: Optional[str]


class Tournament(Document):
    _id: PydanticObjectId
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
    _id: PydanticObjectId
    sofascore_id: int
    tournament: Link[Tournament]
    name: str
    year: str

    class Settings:
        name = "tournamentseasons"


class TournamentGroup(Document):
    _id: PydanticObjectId
    sofascore_id: int
    season: Link[TournamentSeason]
    tournament: Link[Tournament]
    name: str

    class Settings:
        name = "tournamentgroups"


class Team(Document):
    _id: PydanticObjectId
    sofascore_id: int
    name: str
    name_code: str
    country: Optional[str] = None
    ranking: Optional[int] = None
    slug: str

    class Settings:
        name = "teams"


class TeamScores(BaseModel):
    period1: int | None = None
    period2: int | None = None
    normaltime: int | None = None
    extratime: int | None = None
    penalties: int | None = None


class TournamentEvent(Document):
    _id: PydanticObjectId
    sofascore_id: int
    stage: Optional[Link[TournamentGroup]]
    slug: Optional[str]
    tournament: Link[Tournament]
    home_team: Link[Team]
    away_team: Link[Team]
    home_score: TeamScores
    away_score: TeamScores
    has_xg: bool = False
    has_eventplayer_statistics: bool = False
    has_eventplayer_heatmap: bool = False
    detail_id: Optional[int]

    class Settings:
        name = "tournamentevents"


BEANIE_MODELS = [
    Tournament,
    TournamentSeason,
    TournamentGroup,
    Team,
    TournamentEvent
]
