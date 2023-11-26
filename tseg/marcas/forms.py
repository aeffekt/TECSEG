from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Marca

class MarcaForm(FlaskForm):	
	def __init__(self, objeto=None):
		super(MarcaForm, self).__init__()  # Llamar al constructor de la clase padre
		self.objeto = objeto

	nombre = StringField('Nombre', validators=[DataRequired()])		
	submit = SubmitField('Crear / Actualizar')

	def validate_nombre(self, nombre):
		if self.objeto:				
				object_already_exist = Marca.query.filter(
								Marca.nombre == nombre.data,
								Marca.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:			
			object_already_exist = Marca.query.filter(
							Marca.nombre == nombre.data).first() # aqui se presenta la edicion del title de un ITEM registrado
		if object_already_exist:
			raise ValidationError('Ese Nombre de Marca ya existe. Por favor, ingrese uno diferente')
		