from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime
from tseg.models import Marca, TipoModelo, Modelo


class ModeloForm(FlaskForm):
	def __init__(self, objeto=None):
		super(ModeloForm, self).__init__()  # Llamar al constructor de la clase padre
		self.marca.choices = [(marca.id ,marca.nombre) for marca in Marca.query.order_by(Marca.id).all()]
		self.marca.choices.insert(0,(-1, ''))
		self.tipo_modelo.choices = [(tipoModelo.id ,tipoModelo.tipo) for tipoModelo in TipoModelo.query.order_by(TipoModelo.id).all()]
		self.tipo_modelo.choices.insert(0,(-1, ''))
		self.anio.choices = [f"'{str(year)[2:]}" for year in range(datetime.now().year + 1, 1999, -1)]
		self.anio.choices.insert(0,'')
		self.objeto = objeto

	marca = SelectField('Marca',coerce=int, validators=[DataRequired()])
	nombre = StringField('Nombre', validators=[DataRequired()])
	anio = SelectField('Año del modelo', validate_choice=False)
	tipo_modelo = SelectField('Tipo de equipo',coerce=int, validators=[DataRequired()])
	descripcion = TextAreaField('Descripción')
	picture = FileField('Imagen de equipo', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif', 'webp', 'jpeg'])])
	submit = SubmitField('Crear / Actualizar')

	def validate_nombre(self, field):
		if self.objeto:				
				object_already_exist = Modelo.query.filter(
								Modelo.nombre == self.nombre.data,
								Modelo.anio == self.anio.data,
								Modelo.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:			
			object_already_exist = Modelo.query.filter(
							Modelo.nombre == self.nombre.data,
							Modelo.anio == self.anio.data).first() # aqui se presenta la edicion del title de un ITEM registrado
		if object_already_exist:
			raise ValidationError('Ese nombre y año de modelo ya existe. Por favor, ingrese uno diferente')


	# Validación de valor NULL para anio
	def validate_anio(self, anio):	
		if anio.data == ' ':
			anio.data=None
			