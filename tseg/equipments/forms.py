from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Client
from tseg import db

class EquipmentForm(FlaskForm):
	def __init__(self):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.owner.choices = [f'[{c.id}] {c.client_name}, {c.business_name}' for c in Client.query.all()]

	title = StringField('Nombre', validators=[DataRequired()])
	numSerie = StringField('Número de serie')
	content = TextAreaField('Descripción')
	owner = SelectField('Cliente',coerce=str, validate_choice=False, validators=[DataRequired()])
	submit = SubmitField('Crear / Actualizar')