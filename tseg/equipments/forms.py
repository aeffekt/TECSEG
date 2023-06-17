from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Client
from tseg import db
from datetime import datetime

class EquipmentForm(FlaskForm):
	def __init__(self):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.owner.choices = [f'[{c.id}] {c.client_name}, {c.business_name}' for c in Client.query.all()]
		self.anio.choices = [str(year) for year in range(2000, datetime.now().year + 2)]
		self.anio.choices.insert(0,'N/D') # agrega item

	title = StringField('Nombre', validators=[DataRequired()])
	numSerie = StringField('Número de serie')
	anio = SelectField('Año de fabricación',coerce=str, validate_choice=False)
	content = TextAreaField('Descripción')
	owner = SelectField('Cliente',coerce=str, validate_choice=False, validators=[DataRequired()])
	submit = SubmitField('Crear / Actualizar')