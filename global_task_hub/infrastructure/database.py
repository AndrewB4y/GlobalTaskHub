import os
from typing import List, Optional
from uuid import UUID

from sqlalchemy import create_engine, Column, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from global_task_hub.domain.entities import Task, TaskStatus
from global_task_hub.domain.interfaces import TaskRepository

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(
        String, primary_key=True, index=True
    )  # Storing UUID as string for SQLite compatibility
    title = Column(String, index=True)
    description = Column(String)
    status = Column(SAEnum(TaskStatus), default=TaskStatus.PENDING)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def to_entity(self) -> Task:
        return Task(
            id=UUID(self.id),
            title=self.title,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(task: Task) -> "TaskModel":
        return TaskModel(
            id=str(task.id),
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db_session):
        self.db = db_session

    def save(self, task: Task) -> Task:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == str(task.id)).first()
        if db_task:
            db_task.title = task.title
            db_task.description = task.description
            db_task.status = task.status
            db_task.updated_at = task.updated_at
        else:
            db_task = TaskModel.from_entity(task)
            self.db.add(db_task)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task.to_entity()

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
        if db_task:
            return db_task.to_entity()
        return None

    def get_all(self) -> List[Task]:
        db_tasks = self.db.query(TaskModel).all()
        return [t.to_entity() for t in db_tasks]

    def delete(self, task_id: UUID) -> None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
