from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from tseg.models import User, Role
from tseg import db

class SearchForm(FlaskForm):
	searched = StringField('Buscar palabra', validators=[DataRequired()])
	submit = SubmitField('Buscar')


class LoginForm(FlaskForm):
	username = StringField('Nombre de usuario',
						validators=[DataRequired(), Length(min=2, max=30)], render_kw={'autofocus': True})
	password = PasswordField('Contraseña',
						validators=[DataRequired(), Length(min=0, max=128)])
	remember = BooleanField('Recordarme')
	submit = SubmitField('Iniciar Sesión')


class RegistrationForm(LoginForm):
	def __init__(self):
		super(RegistrationForm, self).__init__()  # Llamar al constructor de la clase padre
		self.role.choices = [r.role_name for r in Role.query.all()]
		self.role.choices.insert(0,'')

	email = StringField('Email', validators=[DataRequired(), Email()])
	role = SelectField('Tipo de usuario', coerce=str, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'}) # validate_choice=F si no hay error de validacion
	confirm_password = PasswordField('Confirmar Contraseña', 
						validators=[DataRequired(), EqualTo('password'), Length(min=4, max=12)])
	submit = SubmitField('Registrar Usuario')

	# custom validators = validator_{field_name}
	def validate_username(self, username):
		if ' ' in username.data:
			raise ValidationError('El nombre de usuario no puede contener espacios')
		name_already_exist = User.query.filter_by(username=username.data).first()
		if name_already_exist:
			raise ValidationError('Ese nombre ya está en uso. Por favor, elija uno diferente')
		


	def validate_email(self, email):
		mail_already_exist = User.query.filter_by(email=email.data).first()
		if mail_already_exist:
			raise ValidationError('Ese Email ya está en uso. Por favor, elija uno diferente')


class UpdateAccountForm(FlaskForm):
	def __init__(self):
		super(UpdateAccountForm, self).__init__()  # Llamar al constructor de la clase padre
		self.role.choices = [r for r in Role.query.all()]

	username = StringField('Nombre de usuario',
						validators=[DataRequired(), Length(min=2, max=30)], 
						render_kw={'autofocus': True})
	email = StringField('Email', validators=[DataRequired(), Email()])
	role = SelectField('Tipo de usuario', choices=[], 
										coerce=str, 
										validate_choice=False) # validate_choice=F si no hay error de validacion
	picture = FileField('Imagen de usuario', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif'])])
	submit = SubmitField('Modificar cuenta')

	# custom validators = validator_{field_name}
	def validate_username(self, username):		
		if ' ' in username.data:
			raise ValidationError('El nombre de usuario no puede contener espacios')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Resetear contraseña.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ese email no se encuentra en nuestros registros. Debe crear una cuenta primero.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Aplicar nueva contraseña.')