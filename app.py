from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse

from database import db_lifespan
from tasks import create_task

app: FastAPI = FastAPI(lifespan=db_lifespan)


@app.get("/", tags=['home'])
async def home():
    return {
        "message": "Hello, Friend!",
    }


@app.post("/task")
def run_task(data=Body(...)):
    amount = int(data['amount'])
    x = data['x']
    y = data['y']
    task = create_task.delay(amount, x, y)

    return JSONResponse({"task": task.get()})
