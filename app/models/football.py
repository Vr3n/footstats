from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, SQLModel, Relationship

from app.models.base import TimestampMixin, IdMixin


class Base(IdMixin, TimestampMixin):
    pass


class CategoryBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    name: str
    slug: str | None


class Category(Base, CategoryBase, table=True):
    __tablename__ = "category"

    tournaments: List["Tournament"] = Relationship(back_populates="category",
                                                   sa_relationship_kwargs={
                                                       "lazy": "selectin",
                                                   })


class CategoryPublic(CategoryBase):
    pass


class PublicCategoryWithTournament(CategoryBase):
    tournaments: List["TournamentBase"] | None = None


class TournamentBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    name: str
    slug: Optional[str] = None
    has_standings_groups: bool = False
    has_groups: bool = False
    has_rounds: bool = False
    has_playoff_series: bool = False
    sofascore_link: Optional[str] = ''
    start_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None

    category_id: int | None = Field(default=None,
                                    foreign_key="category.sofascore_id",)


class Tournament(Base, TournamentBase, table=True):
    __tablename__ = "tournament"

    category: Category | None = Relationship(back_populates="tournaments",
                                             sa_relationship_kwargs={
                                                 "lazy": "selectin",
                                             })

    seasons: List["TournamentSeason"] = Relationship(
        back_populates="tournament",
        sa_relationship_kwargs={
            "lazy": "selectin"
        })

    events: List["TournamentEvent"] | None = Relationship(
        back_populates="tournament",
        sa_relationship_kwargs={
            "lazy": "selectin"
        }
    )


class TournamentWithCategoryPublic(TournamentBase):
    category: CategoryBase | None = None


class TournamentSeasonBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    tournament_id: int = Field(foreign_key="tournament.sofascore_id")
    name: str
    year: str


class TournamentSeason(Base, TournamentSeasonBase, table=True):
    __tablename__ = "tournament_season"

    tournament: Optional[Tournament] = Relationship(back_populates="seasons")

    groups: List["TournamentGroup"] = Relationship(
        back_populates="tournament_season")


class PublicTournamentSeasonWithTournaments(TournamentSeasonBase):
    tournament: TournamentBase | None = None


class TournamentGroupBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    tournament_season_id: int = Field(
        foreign_key="tournament_season.sofascore_id")
    name: str


class TournamentGroup(Base, TournamentGroupBase, table=True):
    __tablename__ = "tournament_group"

    tournament_season: TournamentSeason = Relationship(
        back_populates="groups"
    )

    stages: Optional["TournamentEvent"] = Relationship(
        back_populates="stage"
    )


class TeamBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    name: str
    name_code: str
    country: str | None = None
    ranking: str | None = None
    slug: str


class Team(Base, TeamBase, table=True):
    __tablename__ = "team"

    home_events: List["TournamentEvent"] | None = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={
            'primaryjoin': 'TournamentEvent.home_team_id == Team.sofascore_id',
            "lazy": 'joined',
        }
    )

    away_events: List["TournamentEvent"] | None = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={
            'primaryjoin': 'TournamentEvent.away_team_id == Team.sofascore_id',
            "lazy": 'joined',
        })


class TournamentEventBase(SQLModel):
    sofascore_id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(default=None)
    detail_id: int | None = Field(default=None)

    stage_id: int | None = Field(
        default=None, foreign_key="tournament_group.sofascore_id")

    tournament_id: int = Field(foreign_key="tournament.sofascore_id")

    home_team_id: int = Field(foreign_key="team.sofascore_id")

    away_team_id: int = Field(foreign_key="team.sofascore_id")

    status_code: int | None = Field(default=None)
    status_description: str | None = Field(default=None)
    status_type: str | None = Field(default=None)

    home_score_current: int = Field(default=0)
    home_score_period_1: int = Field(default=0)
    home_score_period_2: int = Field(default=0)
    home_score_normaltime: int = Field(default=0)
    home_score_extratime: int = Field(default=0)
    home_score_penalties: int = Field(default=0)

    away_score_current: int = Field(default=0)
    away_score_period_1: int = Field(default=0)
    away_score_period_2: int = Field(default=0)
    away_score_normaltime: int = Field(default=0)
    away_score_extratime: int = Field(default=0)
    away_score_penalties: int = Field(default=0)

    has_xg: bool = Field(default=False)
    has_eventplayer_statistics: bool = Field(default=False)
    has_eventplayer_heatmap: bool = Field(default=False)

    start_timestamp: datetime | None = Field(default=None)
    end_timestamp: datetime | None = Field(default=None)


class TournamentEvent(Base, TournamentEventBase, table=True):
    __tablename__ = "tournament_event"

    stage: Optional[TournamentGroup] = Relationship(back_populates="stages")

    tournament: Tournament = Relationship(back_populates="events")

    home_team: Team | None = Relationship(
        back_populates='home_events',
        sa_relationship_kwargs={
            'primaryjoin': 'TournamentEvent.home_team_id == Team.sofascore_id',
            "lazy": 'joined',
        }
    )

    away_team: Team | None = Relationship(
        back_populates='away_events',
        sa_relationship_kwargs={
            'primaryjoin': 'TournamentEvent.away_team_id == Team.sofascore_id',
            "lazy": 'joined',
        })


class PublicTournamentWithSeasons(TournamentWithCategoryPublic):
    seasons: List[TournamentSeasonBase] | None = None
