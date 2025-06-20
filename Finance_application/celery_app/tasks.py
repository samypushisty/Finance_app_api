import requests
from celery_app.app import celery_app
from celery_app.config import  settings
from core.redis_db.redis_helper import  redis_local_client


@celery_app.task(
    name='update_prices',
)
def update_prices():
    try:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{settings.API_key}/latest/USD")
        response = response.json()["conversion_rates"]
        for k,v in response.items():
            redis_local_client.set(k, v)
        return "Success"
    except Exception as e:
        return e
