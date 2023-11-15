from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Modelo, Homologacion

class HomologacionForm(FlaskForm):
	def __init__(self, objeto=None):
		super(HomologacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.modelo.choices = [modelo.nombre for modelo in Modelo.query.all()]
		self.modelo.choices.insert(0,'')
		self.objeto = objeto

	modelo = SelectField('Modelo',coerce=str, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'})
	codigo = StringField('Código', validators=[DataRequired()])	
	submit = SubmitField('Aceptar')

	def validate_codigo(self, codigo):
		if ' ' in codigo.data:
			raise ValidationError('El código no puede contener espacios')
		if self.objeto:				
				object_already_exist = Homologacion.query.filter(
								Homologacion.codigo == codigo.data,
								Homologacion.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:			
			object_already_exist = Homologacion.query.filter(
							Homologacion.codigo == codigo.data).first() # aqui se presenta la edicion del title de un ITEM registrado
		if object_already_exist:
			raise ValidationError('Ese Código de Homologación ya existe. Por favor, ingrese uno diferente')
	
	def validate_modelo(self, modelo):		
		if self.objeto:				
				object_already_exist = Homologacion.query.filter(
								Homologacion.modelo == modelo.data,
								Homologacion.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:			
			object_already_exist = Homologacion.query.filter(
							Homologacion.modelo == modelo.data).first() # aqui se presenta la edicion del title de un ITEM registrado
		if object_already_exist:
			raise ValidationError('Ese Modelo ya cuenta con un Código de Homologación registrado. Seleccione otro modelo.')
