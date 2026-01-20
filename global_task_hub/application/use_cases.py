from typing import List
from uuid import UUID

from global_task_hub.domain.entities import Task
from global_task_hub.domain.interfaces import TaskRepository, TaskEventPublisher

class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description)
        return self.repository.save(task)

class CompleteTaskUseCase:
    def __init__(self, repository: TaskRepository, event_publisher: TaskEventPublisher = None):
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, task_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        
        task.complete()
        updated_task = self.repository.save(task)
        
        if self.event_publisher:
            self.event_publisher.publish_completed(updated_task)
            
        return updated_task

class GetTasksUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self) -> List[Task]:
        return self.repository.get_all()
