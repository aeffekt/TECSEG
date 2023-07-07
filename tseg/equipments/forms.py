from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Client, Marca, Modelo, Frecuencia, Equipment
from tseg import db
from datetime import datetime

class EquipmentForm(FlaskForm):
	def __init__(self):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.marca.choices = [marca.nombre for marca in Marca.query.all()]
		self.marca.choices.insert(0,'')
		self.modelo.choices = [mod.nombre for mod in Modelo.query.all()]
		self.frecuencia.choices = [f.canal for f in Frecuencia.query.all()]
		self.owner.choices = [f'[{c.id}] {c.nombre} {c.apellido}, {c.business_name}' for c in Client.query.all()]		
		self.owner.choices.insert(0,'') # agrega item "sin datos"
		self.anio.choices = [int(year) for year in range(datetime.now().year + 1, 1999, -1)]
		self.anio.choices.insert(0,'N/D') # agrega item "sin datos"
		

	marca = SelectField('Marca',coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})
	modelo = SelectField('Modelo',coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})
	frecuencia = SelectField('Canal / Frecuencia',coerce=str, render_kw={'data-placeholder': 'Seleccione un item...'})
	numSerie = StringField('Número de serie', validators=[DataRequired()])
	anio = SelectField('Año de fabricación',coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item'})
	content = TextAreaField('Descripción')
	owner = SelectField('Cliente',coerce=str, validate_choice=False, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item'})
	submit = SubmitField('Crear / Actualizar')	