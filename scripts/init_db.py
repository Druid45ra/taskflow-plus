import json
from app.core.database import SessionLocal
from app.users.models import User

def load_mock_users():
    with open("app/users/users.json", "r") as f:
        users = json.load(f)
        db = SessionLocal()
        for user_data in users:
            db.add(User(**user_data))
        db.commit()
