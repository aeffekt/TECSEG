from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Client, Marca, Modelo, Frecuencia
from tseg import db
from datetime import datetime

class EquipmentForm(FlaskForm):
	def __init__(self):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.marca.choices = [marca.nombre for marca in Marca.query.all()]
		self.modelo.choices = [mod.nombre for mod in Modelo.query.all()]
		self.frecuencia.choices = [f.canal for f in Frecuencia.query.all()]
		self.owner.choices = [f'[{c.id}] {c.nombre} {c.nombre}, {c.business_name}' for c in Client.query.all()]
		self.anio.choices = [int(year) for year in range(datetime.now().year + 1, 1979, -1)]
		self.anio.choices.insert(0,'N/D') # agrega item "sin datos"

	marca = SelectField('Marca',coerce=str, validate_choice=False, validators=[DataRequired()])
	modelo = SelectField('Modelo',coerce=str, validate_choice=False, validators=[DataRequired()])	
	frecuencia = SelectField('Canal / Frecuencia',coerce=str)
	numSerie = StringField('Número de serie')
	anio = SelectField('Año de fabricación',coerce=str, validate_choice=False)
	content = TextAreaField('Descripción')	
	owner = SelectField('Cliente',coerce=str, validate_choice=False, validators=[DataRequired()])
	submit = SubmitField('Crear / Actualizar')
