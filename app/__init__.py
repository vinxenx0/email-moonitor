# __init__py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, current_user

# Configurar el registro
#logging.basicConfig(filename='instance/error.log', level=logging.ERROR)

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#@app.errorhandler(Exception)
#def handle_exception(error):
#    app.logger.error('Unhandled Exception: %s', error)
#    return 'Internal Server Error', 500

# Importar modelos y vistas

from app.controllers import main_controller, user_controller, tools_controller
from app.views import user_views, tools_views
from app.models.user_model import User
from app.forms import LoginForm, ConfigForm

# Comprobamos si la base de datos SQLite existe, y si no, la creamos
database_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
if not os.path.exists(database_path):
    open(database_path, 'w').close()


# Crear la primera instancia de usuario si no existe
with app.app_context():
    db.create_all()
    if not User.query.first():
        new_user = User(username='user', email='example@example.com', role='usuario', 
                        config = {"color_primary": "#ffffff", "color_secondary": "#000000", "color_tertiary": "#0066cc", 
                                  "web_name": "WHITE", "logo_url": "https://web.com/asdfadsf.png"}
                        )
        new_user.set_password('user')
        db.session.add(new_user)
        db.session.commit()

        new_admin = User(username='admin', email='admin@example.com', role='admin', 
                        config = {"color_primary": "#ffffff", "color_secondary": "#000000", "color_tertiary": "#0066cc", 
                                  "web_name": "WHITE", "logo_url": "https://web.com/asdfadsf.png"}
                        )
        new_admin.set_password('admin')
        db.session.add(new_admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_sidebar_info():
    return dict(is_admin=current_user.is_authenticated and current_user.role == 'admin')
