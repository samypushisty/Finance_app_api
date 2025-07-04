from celery import Celery
from datetime import timedelta

from core.redis_db.redis_helper import redis_url

celery_app = Celery(
    "celery_worker",  # Имя приложения Celery
    broker_connection_retry_on_startup = True,
    broker=redis_url,  # URL брокера задач (Redis)
    include="celery_app.tasks"
)

celery_app.conf.beat_schedule = {
    "update_prices": {
        "task": 'update_prices',
        "schedule": timedelta(hours=1)
    },
    "balances_history": {
        "task": 'balances_history',
        "schedule": timedelta(days=1)
    }
}
