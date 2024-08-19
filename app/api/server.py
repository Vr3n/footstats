import warnings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.utils import create_db_and_tables
from app.core.config import settings

from app.api.routes import router as api_router
from app.db.session import engine

warnings.filterwarnings(
    "ignore", category=UserWarning, message=r'.*PydanticJsonSchemaWarning.*'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(engine)
    yield


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        lifespan=lifespan
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()


# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables(engine)


@app.get("/", tags=['health'])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )
