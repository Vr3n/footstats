import time
from celery import Celery
from settings import settings


celery_app = Celery(__name__, broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_RESULT_BACKEND)


@celery_app.task
def create_task(a, b, c):
    time.sleep(a)
    return b + c
