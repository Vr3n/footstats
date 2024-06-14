import sentry_sdk
from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

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
