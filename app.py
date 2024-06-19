import sentry_sdk
from typing import Annotated, Dict, List
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles

from crud.tournament import create_tournament
from models.documents import Tournament, TournamentSeason
from settings import settings
from database import db_lifespan
from logger import logger
from scraping.scrape_euro_league import euro_scraper
from main import templates


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app: FastAPI = FastAPI(lifespan=db_lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=['home'])
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/tournaments")
async def all_tournaments() -> List[Tournament] | Dict:
    tournaments = await Tournament.all().to_list()

    if not tournaments:
        return {
            "message": "No Tournaments added!"
        }

    return tournaments


@app.post("/tournaments")
async def add_tournament(tournament: Tournament) -> Tournament:
    tournament = await create_tournament(tournament)
    return tournament


@app.get("/scrape-euro-league")
async def fetch_euro_league():
    await euro_scraper.run_scraper()

    return {
        "message": "Scraping Completed Successfully!"
    }
