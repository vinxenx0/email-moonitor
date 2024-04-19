# __init__py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Configurar el registro
#logging.basicConfig(filename='error.log', level=logging.ERROR)

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error('Unhandled Exception: %s', error)
    #return 'Internal Server Error', 500

# Importar modelos y vistas

from app.controllers import main_controller, user_controller
