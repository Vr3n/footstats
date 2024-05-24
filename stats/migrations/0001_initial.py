# Generated by Django 4.2.13 on 2024-05-23 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='City Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='City Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='Continent Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Continent Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='Country Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Country Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='League Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='League Slug')),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.continent')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeagueSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Season Start')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Season End')),
                ('name', models.CharField(max_length=250, verbose_name='Season Name')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.league')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeagueStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Stage Slug')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Stage Start')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Stage End')),
                ('league_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leagueseason')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=256, verbose_name='Manager Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Manager Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MatchScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_time', models.PositiveBigIntegerField(default=0)),
                ('half_1', models.PositiveBigIntegerField(default=0)),
                ('half_2', models.PositiveBigIntegerField(default=0)),
                ('extra_1', models.PositiveBigIntegerField(default=0)),
                ('extra_2', models.PositiveBigIntegerField(default=0)),
                ('overtime', models.PositiveBigIntegerField(default=0)),
                ('aggregated', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='Team Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Team Slug')),
                ('short_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Abbrevation')),
                ('name_code', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name Code')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamSeasonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('points', models.PositiveIntegerField(default=0)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('matches_played', models.PositiveIntegerField(default=0)),
                ('league_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leagueseason')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MatchVenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('stadium_name', models.CharField(max_length=250, verbose_name='Match Venue')),
                ('stadium_capacity', models.PositiveIntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('start_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Match Commenced On')),
                ('end_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Match Ended On')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Match Slug')),
                ('away_score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_score', to='stats.matchscore')),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='stats.team')),
                ('home_score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_score', to='stats.matchscore')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='stats.team')),
                ('league_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leagueseason')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManagerSeasonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('league_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leagueseason')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.manager')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeagueStageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('code', models.CharField(max_length=256, verbose_name='Stage Status code')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('status_type', models.CharField(blank=True, max_length=256, null=True)),
                ('league_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.leaguestage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]