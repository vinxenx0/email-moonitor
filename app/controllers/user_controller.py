# controllers/user_controller.py
from app.models.user_model import User
from app import db

def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
