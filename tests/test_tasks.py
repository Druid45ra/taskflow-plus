import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.users.models import User
from app.tasks.models import Task
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_taskflow.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test User",
        is_active=True,
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield db, user
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_task(setup_database):
    db, user = setup_database
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "deadline": "2023-12-31T23:59:59",
            "priority": "High",
            "status": "Pending",
            "owner_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "High"
    assert data["status"] == "Pending"
    assert data["owner"]["email"] == "testuser@example.com"

def test_get_task(setup_database):
    db, user = setup_database
    task = Task(
        title="Existing Task",
        description="This task already exists",
        deadline="2023-12-31T23:59:59",
        priority="Medium",
        status="Pending",
        owner_id=user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Existing Task"
    assert data["description"] == "This task already exists"
    assert data["priority"] == "Medium"
    assert data["status"] == "Pending"
    assert data["owner"]["email"] == "testuser@example.com"

def test_update_task(setup_database):
    db, user = setup_database
    task = Task(
        title="Task to Update",
        description="This task will be updated",
        deadline="2023-12-31T23:59:59",
        priority="Low",
        status="Pending",
        owner_id=user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.put(
        f"/tasks/{task.id}",
        json={
            "title": "Updated Task",
            "description": "This task has been updated",
            "deadline": "2023-12-31T23:59:59",
            "priority": "High",
            "status": "Completed",
            "owner_id": user.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "This task has been updated"
    assert data["priority"] == "High"
    assert data["status"] == "Completed"
    assert data["owner"]["email"] == "testuser@example.com"

def test_delete_task(setup_database):
    db, user = setup_database
    task = Task(
        title="Task to Delete",
        description="This task will be deleted",
        deadline="2023-12-31T23:59:59",
        priority="Low",
        status="Pending",
        owner_id=user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Task deleted successfully"
    
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 404
