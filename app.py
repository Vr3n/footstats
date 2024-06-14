import sentry_sdk
from typing import Annotated, Dict, List
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

from crud.tournament import create_tournament
from models.documents import Tournament, TournamentSeason
from scraping.scrape_euro_league import (
    extract_and_store_tournament_details, extract_and_store_tournament_seasons)
from settings import settings
from database import db_lifespan
from tasks import create_task


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app: FastAPI = FastAPI(lifespan=db_lifespan)


@app.get("/", tags=['home'])
async def home():
    return {
        "message": "Hello, Friend!",
    }


@app.post("/task")
def run_task(amount: Annotated[int, Form()], x: Annotated[int, Form()],
             y: Annotated[int, Form()]):
    amount = int(amount)
    x = int(x)
    y = int(y)
    task = create_task.delay(amount, x, y)

    return JSONResponse({"task": task.get()})


@app.get("/fetch-tournament-seasons")
async def fetch_tournaments_seasons() -> List[TournamentSeason]:
    seasons = await extract_and_store_tournament_seasons()

    return seasons


@app.get("/tournaments")
async def all_tournaments() -> List[Tournament] | Dict:
    tournaments = await Tournament.all().to_list()

    if not tournaments:
        return {
            "message": "No Tournaments added!"
        }

    return JSONResponse(tournaments)


@app.post("/tournaments")
async def add_tournament(tournament: Tournament) -> Tournament:
    tournament = await create_tournament(tournament)
    return tournament


@app.get("/fetch-euro-league")
async def fetch_euro_league() -> Tournament:
    tournament = await extract_and_store_tournament_details()

    return tournament
