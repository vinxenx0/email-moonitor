# __init__py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager

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
from app.models import user_model
from app.forms import LoginForm