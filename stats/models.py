from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BaseModel(models.Model):
    """
    Contains Common fields used in every model.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    sofascore_id = models.CharField(
        _("SofaScore Id"), max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


class TournamentCategory(BaseModel):
    """
    Tournament Category.
    """

    name = models.CharField(_("Category Name"), max_length=250)
    slug = models.SlugField(_("Continent Slug"), null=True, blank=True)


class Continent(BaseModel):
    name = models.CharField(_("Continent Name"), max_length=250)
    slug = models.SlugField(_("Continent Slug"), null=True, blank=True)


class Country(BaseModel):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    name = models.CharField(_("Country Name"), max_length=250)
    slug = models.SlugField(_("Country Slug"), null=True, blank=True)


class City(BaseModel):
    name = models.CharField(_("City Name"), max_length=250)
    slug = models.SlugField(_("City Slug"), null=True, blank=True)


class League(BaseModel):
    tournament_category = models.ForeignKey(
        TournamentCategory, on_delete=models.CASCADE, null=True, blank=True)
    continent = models.ForeignKey(
        Continent, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_("League Name"), max_length=250)
    slug = models.SlugField(_("League Slug"), null=True, blank=True)


class Team(BaseModel):
    name = models.CharField(_("Team Name"), max_length=250)
    slug = models.SlugField(_("Team Slug"), null=True, blank=True)
    short_name = models.CharField(
        _("Abbrevation"), max_length=250, null=True, blank=True)
    name_code = models.CharField(
        _("Name Code"), max_length=250, null=True, blank=True)


class LeagueSeason(BaseModel):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    start_date = models.DateField(_("Season Start"), null=True, blank=True)
    end_date = models.DateField(_("Season End"), null=True, blank=True)
    name = models.CharField(_("Season Name"), max_length=250)


class Manager(BaseModel):
    name = models.CharField(_("Manager Name"), max_length=256)
    slug = models.SlugField(_("Manager Slug"), null=True, blank=True)


class TeamSeasonHistory(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league_season = models.ForeignKey(LeagueSeason, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    matches_played = models.PositiveIntegerField(default=0)


class ManagerSeasonHistory(BaseModel):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    league_season = models.ForeignKey(LeagueSeason, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class LeagueStage(BaseModel):
    league_season = models.ForeignKey(LeagueSeason, on_delete=models.CASCADE)
    slug = models.SlugField(_("Stage Slug"), null=True, blank=True)
    start_date = models.DateField(_("Stage Start"), null=True, blank=True)
    end_date = models.DateField(_("Stage End"), null=True, blank=True)


class LeagueStageStatus(BaseModel):
    league_stage = models.ForeignKey(LeagueStage, on_delete=models.CASCADE)
    code = models.CharField(_("Stage Status code"), max_length=256)
    description = models.CharField(
        _("Description"), max_length=256, null=True, blank=True)
    status_type = models.CharField(max_length=256, null=True, blank=True)


class MatchScore(models.Model):
    normal_time = models.PositiveBigIntegerField(default=0)
    half_1 = models.PositiveBigIntegerField(default=0)
    half_2 = models.PositiveBigIntegerField(default=0)
    extra_1 = models.PositiveBigIntegerField(default=0)
    extra_2 = models.PositiveBigIntegerField(default=0)
    overtime = models.PositiveBigIntegerField(default=0)
    aggregated = models.PositiveBigIntegerField(default=0)


class Match(BaseModel):
    league_season = models.ForeignKey(LeagueSeason, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField(
        _("Match Commenced On"), null=True, blank=True)
    end_date_time = models.DateTimeField(
        _("Match Ended On"), null=True, blank=True)
    home_team = models.ForeignKey(
        Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(
        Team, related_name='away_team', on_delete=models.CASCADE)
    home_score = models.ForeignKey(
        MatchScore, related_name='home_score', on_delete=models.CASCADE, )
    away_score = models.ForeignKey(
        MatchScore, related_name='away_score', on_delete=models.CASCADE, )
    slug = models.SlugField(_("Match Slug"), null=True, blank=True)


class MatchVenue(BaseModel):
    stadium_name = models.CharField(_("Match Venue"), max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    stadium_capacity = models.PositiveIntegerField(default=0)
