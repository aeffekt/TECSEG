from flask_login import current_user
from flask_wtf import FlaskForm
from flask import flash
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tseg.models import User, Role
from tseg import bcrypt

class SearchForm(FlaskForm):
	searched = StringField('Buscar palabra', validators=[DataRequired()])
	submit = SubmitField('Buscar')


class LoginForm(FlaskForm):
	username = StringField('Nombre de usuario',
						validators=[DataRequired(), Length(min=2, max=30)], render_kw={'autofocus': True})
	password = PasswordField('Contraseña',
						validators=[DataRequired(), Length(min=4, max=12)])
	remember = BooleanField('Recordarme')
	submit = SubmitField('Iniciar Sesión')


class RegistrationForm(LoginForm):
	def __init__(self):
		super(RegistrationForm, self).__init__()  # Llamar al constructor de la clase padre
		self.role.choices = [(r.id, r.role_name) for r in Role.query.all()]
		self.role.choices.insert(0,(-1,''))

	email = StringField('Email', validators=[DataRequired(), Email()])
	role = SelectField('Tipo de usuario', coerce=int, validators=[DataRequired()])
	confirm_password = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password'), Length(min=4, max=12)])
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
		self.role.choices = [(r.id, r.role_name) for r in Role.query.all()]

	username = StringField('Nombre de usuario',
						validators=[DataRequired(), Length(min=2, max=30)], 
						render_kw={'autofocus': True})
	email = StringField('Email', validators=[DataRequired(), Email()])
	role = SelectField('Tipo de usuario', coerce=int, validate_choice=False) # validate_choice=F si no hay error de validacion
	picture = FileField('Imagen de usuario', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif'])])
	submit = SubmitField('Actualizar datos de cuenta')

	# custom validators = validator_{field_name}
	def validate_username(self, username):		
		if ' ' in username.data:
			raise ValidationError('El nombre de usuario no puede contener espacios')


class UpdatePassword(FlaskForm):
	old_password = PasswordField('Contraseña Actual',
						validators=[DataRequired(), Length(min=4, max=12)])
	password = PasswordField('Contraseña Nueva',
						validators=[DataRequired(), Length(min=4, max=12)])
	confirm_password = PasswordField('Confirmar Contraseña', 
						validators=[DataRequired(), EqualTo('password'), Length(min=4, max=12)])	
	submit = SubmitField('Actualizar Contraseña')

	def validate_old_password(self, old_password):
		if not bcrypt.check_password_hash(current_user.password, old_password.data):			
			raise ValidationError('La contraseña es incorrecta')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Resetear contraseña')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ese email no se encuentra en nuestros registros. Debe crear una cuenta primero.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Aplicar nueva contraseña.')
	