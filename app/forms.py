# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp, Email, EqualTo, ValidationError
from app.models.user_model import User

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('usuario', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')

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

class PingForm(FlaskForm):
    domain = StringField('Dominio a pingear', validators=[DataRequired()])
    submit = SubmitField('Enviar')