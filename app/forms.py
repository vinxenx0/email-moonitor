from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, URL, Regexp

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ConfigForm(FlaskForm):
    color_primary = StringField('Color primario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    color_secondary = StringField('Color secundario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    color_tertiary = StringField('Color terciario', validators=[DataRequired(), Regexp(r'^#[0-9a-fA-F]{6}$', message='Color debe ser en formato hexadecimal (#RRGGBB)')])
    web_name = StringField('Nombre de la web', validators=[DataRequired()])
    logo_url = StringField('URL del logotipo', validators=[DataRequired(), URL()])

