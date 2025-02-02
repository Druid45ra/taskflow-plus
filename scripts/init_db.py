import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.users.models import User
from app.tasks.models import Task

engine = create_engine("sqlite:///./taskflow.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_mock_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Încarcă utilizatori
    with open("app/users/users.json") as f:
        users = json.load(f)
        for user_data in users:
            db.add(User(**user_data))
    
    # Încarcă sarcini
    with open("app/tasks/tasks.json") as f:
        tasks = json.load(f)
        for task_data in tasks:
            db.add(Task(**task_data))
    
    db.commit()

if __name__ == "__main__":
    load_mock_data()
