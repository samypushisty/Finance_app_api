from abc import abstractmethod
from typing import Protocol, List


class TasksI(Protocol):
    @abstractmethod
    def get_ids_active_users(self) -> List[int]:
        ...