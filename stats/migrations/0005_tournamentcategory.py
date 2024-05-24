# Generated by Django 4.2.13 on 2024-05-24 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_alter_league_continent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('sofascore_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='SofaScore Id')),
                ('name', models.CharField(max_length=250, verbose_name='Category Name')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Continent Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]