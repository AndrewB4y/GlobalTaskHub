from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum, auto


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """
    Task entity representing a unit of work.
    """

    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def complete(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        return self.status == TaskStatus.COMPLETED
