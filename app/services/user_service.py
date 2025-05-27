from app.db.session import SessionLocal
from app.db.models import User

class UserService:
    def __init__(self):
        self.db = SessionLocal()

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
