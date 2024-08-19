from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

from models.base import TimestampMixin


class Base(SQLModel, TimestampMixin):
    sofascore_id: int | None = Field(default=None, primary_key=True)


class Category(Base, table=True):
    __tablename__ = "category"

    sofascore_id: int = Field(default=None, primary_key=True)
    name: str
    slug: str | None
    tournaments: List["Tournament"] = Relationship(back_populates="category")


class Tournament(Base, table=True):
    __tablename__ = "tournament"

    category_id: int = Field(foreign_key="category.sofascore_id")
    category: Category = Relationship(back_populates="tournaments")
    name: str
    slug: Optional[str]
    has_standings_groups: bool = False
    has_groups: bool = False
    has_rounds: bool = False
    has_playoff_series: bool = False
    sofascore_link: Optional[str] = ''
    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]

    seasons: List["TournamentSeason"] = Relationship(
        back_populates="tournament")

    events: List["TournamentEvent"] = Relationship(
        back_populates="tournament"
    )


class TournamentSeason(Base, table=True):
    __tablename__ = "tournament_season"
    tournament_id: int = Field(foreign_key="tournament.sofascore_id")
    tournament: Tournament = Relationship(back_populates="seasons")
    name: str
    year: str

    groups: List["TournamentGroup"] = Relationship(
        back_populates="tournament_season")


class TournamentGroup(Base, table=True):
    __tablename__ = "tournament_group"
    tournament_season_id: int = Field(
        foreign_key="tournament_season.sofacore_id")
    tournament_season: TournamentSeason = Relationship(
        back_populates="groups"
    )
    name: str

    stages: Optional["TournamentEvent"] = Relationship(
        back_populates="stage"
    )


class Team(Base, table=True):
    __tablename__ = "team"

    name: str
    name_code: str
    country: Optional[str] = None
    ranking: Optional[int] = None
    slug: str

    home_events: List["TournamentEvent"] = Relationship(
        back_populates="home_team"
    )

    away_events: List["TournamentEvent"] = Relationship(
        back_populates="away_team"
    )


class TeamScores(SQLModel):
    period1: int | None = None
    period2: int | None = None
    normaltime: int | None = None
    extratime: int | None = None
    penalties: int | None = None


class TournamentEvent(Base):
    __tablename__ = "tournament_event"

    slug: Optional[str]
    detail_id: Optional[int]

    stage_id: Optional[int] = Field(
        default=None, foreign_key="tournament_group.sofascore_id")
    stage: Optional[TournamentGroup] = Relationship(back_populates="stages")

    tournament_id: int = Field(foreign_key="tournament_sofascore_id")
    tournament: Tournament = Relationship(back_populates="events")

    home_team_id: int = Field(foreign_key="team.sofascore_id")
    home_team: Team = Relationship(back_populates="home_events")

    away_team_id: int = Field(foreign_key="team.sofascore_id")
    away_team: Team = Relationship(back_populates="away_events")

    home_score: TeamScores
    away_score: TeamScores

    has_xg: bool = False
    has_eventplayer_statistics: bool = False
    has_eventplayer_heatmap: bool = False
