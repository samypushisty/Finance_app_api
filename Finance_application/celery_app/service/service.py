from datetime import datetime, timedelta, timezone
from typing import Callable, List

from sqlalchemy import select

from celery_app.service.interface import TasksI
from sqlalchemy.orm import  Session

from celery_app.utils.repository import SQLAlchemyRepository
from core.models.base import User


class Tasks(TasksI):
    def __init__(self,repository: SQLAlchemyRepository, database_session:Callable[..., Session]) -> None:
        self.repository = repository
        self.session = database_session

    def get_ids_active_users(self) -> List[int]:
        with self.session() as session:
            with session.begin():
                print(session)
                one_week_ago = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
                query = (
                    select(User.chat_id
                    )
                    .filter(self.repository.model.last_visit >= one_week_ago)
                    .order_by("chat_id")
                )
                result = session.execute(query)
                result = list(result.scalars().all())
                return result