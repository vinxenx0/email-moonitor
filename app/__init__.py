# __init__py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, current_user

# Configurar el registro
#logging.basicConfig(filename='error.log', level=logging.ERROR)

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error('Unhandled Exception: %s', error)
    #return 'Internal Server Error', 500

# Importar modelos y vistas

from app.controllers import main_controller, user_controller
from app.views import user_views
from app.models.user_model import User
from app.forms import LoginForm, ConfigForm


# Crear la primera instancia de usuario si no existe
with app.app_context():
    db.create_all()
    if not User.query.first():
        new_user = User(username='user', email='example@example.com')
        new_user.set_password('user')
        db.session.add(new_user)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_sidebar_info():
    return dict(is_admin=current_user.is_authenticated and current_user.role == 'admin')
