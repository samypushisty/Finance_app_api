from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource
from sqlalchemy.orm import Session
from typing import Generator

from celery_app.service.service import Tasks
from celery_app.service.interface import TasksI

from celery_app.utils.repository import SQLAlchemyRepository
from core.config import settings
from core.models.base import User, MovieOnAccount, Balance
from core.models.db_helper import SyncDatabaseHelper
from core.redis_db.redis_helper import redis_session_getter

class DependencyContainer(containers.DeclarativeContainer):

    database_helper: Singleton["SyncDatabaseHelper"] = Singleton(
        SyncDatabaseHelper,
        url=str(settings.db.sync_url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    database_session: Resource["Generator[Session, None, None]"] = Resource(database_helper.provided.session_getter)

    user_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model = User,
    )

    movies_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=MovieOnAccount,
    )

    balance_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=Balance,
    )

    tasks_service: Factory["TasksI"] = Factory(Tasks,
                                               repository=user_repository,
                                               database_session=database_session)

container = DependencyContainer()