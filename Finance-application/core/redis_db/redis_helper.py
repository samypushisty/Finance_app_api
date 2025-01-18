from core.config import settings
import redis

# Формирование URL для подключения к Redis
redis_url = f"redis://:{settings.db_redis.REDIS_PASSWORD}@{settings.db_redis.REDIS_HOST}:{settings.db_redis.REDIS_PORT}/0"

redis_client = redis.Redis(
    host=settings.db_redis.REDIS_HOST,
    port=settings.db_redis.REDIS_PORT,
    db=0,
    password=settings.db_redis.REDIS_PASSWORD,
)