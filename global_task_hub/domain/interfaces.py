from typing import List, Optional, Protocol
from uuid import UUID
from .entities import Task


class TaskRepository(Protocol):
    """
    Interface for Task storage operations.
    """

    def save(self, task: Task) -> Task:
        """Save text entity."""
        ...

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        ...

    def get_all(self) -> List[Task]:
        """Retrieve all tasks."""
        ...

    def delete(self, task_id: UUID) -> None:
        """Delete a task by its ID."""
        ...


# Event Interface (Optional based on requirements but good for Clean Arch)
class TaskEventPublisher(Protocol):
    def publish_completed(self, task: Task) -> None: ...
