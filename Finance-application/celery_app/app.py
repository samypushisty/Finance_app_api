import requests
from celery import Celery
from celery_app.config import  settings
from datetime import timedelta

from core.redis_db.redis_helper import redis_url, redis_client

celery_app = Celery(
    "celery_worker",  # Имя приложения Celery
    broker_connection_retry_on_startup = True,
    broker=redis_url,  # URL брокера задач (Redis)
)

@celery_app.task(
    name='update_prices',
)
def update_prices():
    try:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{settings.API_key}/latest/USD")
        response = response.json()["conversion_rates"]
        for k,v in response.items():
            redis_client.set(k, v)
        return "Success"
    except Exception as e:
        return e

celery_app.conf.beat_schedule = {
    "update_prices": {
        "task": 'update_prices',
        "schedule": timedelta(seconds=30)
    },
}