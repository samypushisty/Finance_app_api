import requests
from celery import Celery
from celery_app.config import  settings
from datetime import timedelta

from core.redis_db.redis_helper import redis_url

celery_app = Celery(
    "celery_worker",  # Имя приложения Celery
    broker_connection_retry_on_startup = True,
    broker=redis_url,  # URL брокера задач (Redis)
)

@celery_app.task(
    name='get_jwt',
)
def get_jwt(user_id):
    try:
        response = requests.post(f"{settings.BASE_URL}/api/v1/auth", json={"chat_id":user_id})
        response.raise_for_status()
        return response.text
    except Exception as e:
        return e

celery_app.conf.beat_schedule = {
    "get_jwt": {
        "task": 'get_jwt',
        "schedule": timedelta(seconds=30),
        "args": (999999999,)
    },
}