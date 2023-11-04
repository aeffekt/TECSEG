from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Modelo, Frecuencia, Detalle_trabajo
from tseg import db
from datetime import datetime

class EquipmentForm(FlaskForm):
	def __init__(self):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre		
		self.modelo.choices = [(mod.id, f'{mod}-{mod.descripcion}') for mod in Modelo.query.order_by(Modelo.nombre).all()]
		self.modelo.choices.insert(0,(0,'')) # agrega item "sin datos"	
		self.frecuencia.choices = [(f.id, f) for f in Frecuencia.query.all()]
		self.detalle_trabajo.choices = [(d.id, d) for d in Detalle_trabajo.query.all()]
		self.detalle_trabajo.choices.insert(0,(0,'')) # agrega item "sin datos"	
		self.anio.choices = [int(year) for year in range(datetime.now().year + 1, 1999, -1)]
		self.anio.choices.insert(0,'N/D') # agrega item "sin datos"

	modelo = SelectField('Modelo',coerce=int, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})
	frecuencia = SelectField('Canal / Frecuencia',coerce=int, render_kw={'data-placeholder': 'Seleccione un item...'})
	numSerie = StringField('Orden de equipo y Fecha de entrega')
	anio = SelectField('Año de fabricación',coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item'})
	content = TextAreaField('Descripción')
	detalle_trabajo = SelectField('Detalle orden de trabajo',coerce=int, validate_choice=False, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item'})
	submit = SubmitField('Crear / Actualizar')
	