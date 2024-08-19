import asyncio
from httpx import AsyncClient
from arq import create_pool
from arq.connections import RedisSettings
from settings import settings


REDIS_SETTINGS = RedisSettings(
    host="redis",
    port=6379,
    database=settings.CELERY_RESULT_BACKEND
)


async def startup(ctx):
    ctx['session'] = AsyncClient()


async def shutdown(ctx):
    await ctx['session'].aclose()


async def main():
    redis = await create_pool(REDIS_SETTINGS)
