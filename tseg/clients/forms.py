from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField,IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional, Email
from tseg import db
from tseg.models import Pais, Provincia, Cond_fiscal

class ClientForm(FlaskForm):
	def __init__(self):
		super(ClientForm, self).__init__()  # Llamar al constructor de la clase padre		
		self.cond_fiscal.choices = [cond_fiscal.nombre for cond_fiscal in Cond_fiscal.query.all()]

	client_name = StringField('Nombre *', validators=[DataRequired()], render_kw={'autofocus': True})
	business_name = StringField('Razón social')
	cuit = IntegerField('CUIT', validators=[Optional()])
	cond_fiscal = SelectField('Condición fiscal', coerce=str, validate_choice=False)
	telefono = StringField('Teléfono')
	email = StringField('Email', validators=[DataRequired(), Email()])
	comments = TextAreaField('Comentarios')
	domicilio = StringField('Domicilio completo')
	codigo_postal = StringField('Código Postal')
	ciudad = StringField('Ciudad')
	provincia = StringField('Provincia')	
	pais = StringField('Pais')
	submit = SubmitField('Agregar')

	# validacion del CUIT
	def validate_cuit(self, cuit):
		cuit_str = str(cuit.data)
		cant_digitos = len(cuit_str)
		if cant_digitos != 11:
			raise ValidationError(f'Ingresar cuit válido o dejar vacío.')
