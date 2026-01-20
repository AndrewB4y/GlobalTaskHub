import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from global_task_hub.presentation.api import app, get_db
from global_task_hub.infrastructure.database import Base

# Setup In-Memory Database for Testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Important for in-memory SQLite to persist across threads
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_create_and_get_task(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create Task
        response = await ac.post(
            "/tasks/",
            json={"title": "Integration Test Task", "description": "Testing full flow"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Integration Test Task"
        task_id = data["id"]

        # Get Tasks
        response = await ac.get("/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert any(t["id"] == task_id for t in tasks)

        # Complete Task
        response = await ac.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
