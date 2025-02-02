from faker import Faker
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.users.models import User
from app.tasks.models import Task
from app.core.security import get_password_hash

fake = Faker()

def create_fake_user(db: Session):
    user = User(
        email=fake.email(),
        hashed_password=get_password_hash("password"),
        full_name=fake.name(),
        is_active=True,
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_fake_task(db: Session, user_id: int):
    task = Task(
        title=fake.sentence(),
        description=fake.text(),
        deadline=fake.future_datetime(),
        priority=fake.random_element(elements=("Low", "Medium", "High")),
        status="Pending",
        owner_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def generate_mock_data(num_users: int = 10, tasks_per_user: int = 5):
    db = SessionLocal()
    try:
        for _ in range(num_users):
            user = create_fake_user(db)
            for _ in range(tasks_per_user):
                create_fake_task(db, user.id)
    finally:
        db.close()

if __name__ == "__main__":
    generate_mock_data()
