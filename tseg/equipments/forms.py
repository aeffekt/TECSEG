from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField,SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Modelo, Frecuencia, Detalle_trabajo, Equipment, Orden_trabajo
from datetime import datetime
from werkzeug.utils import secure_filename


class EquipmentForm(FlaskForm):
	def __init__(self, objeto=None):
		super(EquipmentForm, self).__init__()  # Llamar al constructor de la clase padre
		self.objeto = objeto
		self.modelo.choices = [(mod.id, f'{mod} -{mod.descripcion[0:35]}') for mod in Modelo.query.order_by(Modelo.nombre).all()]		
		self.modelo.choices.insert(0,(-1,''))
		self.detalle_trabajo.choices = [(d.id, d) for d in Detalle_trabajo.query.all()]		
		self.detalle_trabajo.choices.insert(0,(-1,''))
		self.anio.choices = [int(year) for year in range(datetime.now().year + 1, 1999, -1)]
		self.anio.choices.insert(0,'')
		self.frecuencias.choices = [(f.id, f) for f in Frecuencia.query.all()]
		if objeto:
			self.sistema.choices = [self.objeto.sistema]		
		else:
			self.sistema.choices = [(-1,'')]
		
	modelo = SelectField('Modelo', coerce=int, validate_choice=False, validators=[DataRequired()])
	frecuencias = SelectMultipleField('Canal/es', coerce=int, validate_choice=False)
	numSerie = StringField('Nº serie')
	anio = SelectField('Año de fabricación', coerce=str, validate_choice=False, validators=[DataRequired()])
	content = TextAreaField('Descripción')
	detalle_trabajo = SelectField('Detalle orden de trabajo', coerce=int, validators=[DataRequired()], validate_choice=False)
	sistema = SelectField('Sistema', coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item o creé uno nuevo'})
	upload_files = FileField("Agregar archivos extras")
	submit = SubmitField('Crear / Actualizar')

	def validate_numSerie(self, field):		
		if self.numSerie.data != "" and self.numSerie.data != None:
			if self.objeto:
				ot = self.objeto.detalle_trabajo.orden_trabajo.codigo
				object_already_exist = Equipment.query.join(Detalle_trabajo).join(Orden_trabajo).filter(
									Equipment.numSerie == self.numSerie.data,
									Orden_trabajo.codigo == ot,
									Equipment.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
			else:				
				dt = Detalle_trabajo.query.get(int(self.detalle_trabajo.data))
				ot = dt.orden_trabajo.codigo			
				object_already_exist = Equipment.query.join(Detalle_trabajo).join(Orden_trabajo).filter(
									Equipment.numSerie == self.numSerie.data,
									Orden_trabajo.codigo == ot).first()				
			if object_already_exist:
				raise ValidationError('Ese Nº serie ya está registrado en la misma O.T. Por favor, ingrese uno diferente')
		else:
			self.numSerie.data = None

	def validate_frecuencias(self, frecuencias):	
		if frecuencias.data == 0:
			frecuencias.data=None

	def validate_sistema(self, sistema):	
		if sistema.data == '':
			sistema.data=None
	