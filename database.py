from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from logging import info
from motor.motor_asyncio import AsyncIOMotorClient

from models.documents import BEANIE_MODELS
from settings import settings


@asynccontextmanager
async def db_lifespan(app: FastAPI):

    app.mongodb_client = AsyncIOMotorClient(settings.mongod_uri)
    app.database = app.mongodb_client.get_default_database()

    ping_response = await app.database.command("ping")

    if int(ping_response['ok']) != 1:
        print(ping_response)
        raise Exception("Problem Connecting to database cluster!")
    else:
        info("Connected to database cluster.")

    await init_beanie(database=app.database,
                      document_models=BEANIE_MODELS)

    yield

    app.mongodb_client.close()
