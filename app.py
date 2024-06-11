from fastapi import FastAPI

from database import db_lifespan

app: FastAPI = FastAPI(lifespan=db_lifespan)


@app.get("/", tags=['home'])
async def home():
    return {
        "message": "Hello, Friend!"
    }
