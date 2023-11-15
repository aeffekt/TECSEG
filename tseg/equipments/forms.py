from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Modelo, Frecuencia, Detalle_trabajo, Equipment, Orden_trabajo
from datetime import datetime

class EquipmentForm(FlaskForm):
	def __init__(self, objeto=None):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.objeto = objeto
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
	upload_files = FileField("Subir archivos")
	submit = SubmitField('Crear / Actualizar')

	def validate_numSerie(self, numSerie):		
		if numSerie.data != "" and numSerie.data != None:
			ot = self.objeto.detalle_trabajo.orden_trabajo.codigo
			if self.objeto:					
					object_already_exist = Equipment.query.join(Detalle_trabajo).join(Orden_trabajo).filter(
									Equipment.numSerie == numSerie.data,
									Orden_trabajo.codigo == ot,
									Equipment.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
			else:			
				object_already_exist = Equipment.query.filter(
								Equipment.numSerie == numSerie.data,
								Orden_trabajo.codigo == ot).first() # aqui se presenta la edicion del title de un ITEM registrado
			if object_already_exist:
				raise ValidationError('Ese número de serie ya está registrado en la misma O.T. Por favor, ingrese uno diferente')
	