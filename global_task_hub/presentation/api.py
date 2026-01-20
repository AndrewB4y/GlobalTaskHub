from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from global_task_hub.domain.entities import Task as TaskEntity
from global_task_hub.infrastructure.database import get_db, SQLAlchemyTaskRepository
from global_task_hub.application.use_cases import (
    CreateTaskUseCase,
    CompleteTaskUseCase,
    GetTasksUseCase,
)
from global_task_hub.domain.interfaces import TaskEventPublisher

app = FastAPI(title="GlobalTaskHub API")

import os

# Security/Session Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # nosec
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# i18n Configuration (Simple implementation)
# In a real app, use babel.support.Translations and load .mo files
TRANSLATIONS = {
    "en": {
        "task_created": "Task created successfully",
        "task_completed": "Task completed",
    },
    "es": {
        "task_created": "Tarea creada exitosamente",
        "task_completed": "Tarea completada",
    },
}


def get_locale(request: Request) -> str:
    # Simple locale detection from header
    lang = request.headers.get("Accept-Language", "en")
    return "es" if "es" in lang else "en"


def get_translation(key: str, locale: str) -> str:
    return TRANSLATIONS.get(locale, {}).get(key, key)


# Event System
class APIEventPublisher(TaskEventPublisher):
    def publish_completed(self, task: TaskEntity) -> None:
        print(f"API EVENT: Task '{task.title}' completed via API.")


# Models
class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str

    class Config:
        from_attributes = True


# Routes
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, request: Request, db=Depends(get_db)):
    repo = SQLAlchemyTaskRepository(db)
    use_case = CreateTaskUseCase(repo)
    created_task = use_case.execute(task.title, task.description)

    # Store in session example
    request.session["last_task_id"] = str(created_task.id)

    locale = get_locale(request)
    msg = get_translation("task_created", locale)
    # We could return this msg in a wrapper, but complying with response_model for now.

    return created_task


@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(db=Depends(get_db)):
    repo = SQLAlchemyTaskRepository(db)
    use_case = GetTasksUseCase(repo)
    return use_case.execute()


@app.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: UUID, db=Depends(get_db)):
    repo = SQLAlchemyTaskRepository(db)
    publisher = APIEventPublisher()
    use_case = CompleteTaskUseCase(repo, event_publisher=publisher)
    try:
        return use_case.execute(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/health")
def health_check():
    from global_task_hub.infrastructure.network.health_socket import check_health

    is_online = check_health()
    return {"status": "ok", "network_online": is_online}
