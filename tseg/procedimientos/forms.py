from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Procedimiento


class ProcedimientoForm(FlaskForm):
	def __init__(self, objeto=None):
		super(ProcedimientoForm, self).__init__()
		self.objeto = objeto
	
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Procedimiento')
	submit = SubmitField('Aceptar')

	def validate_title(self, title):		
		if self.objeto:				
				object_already_exist = Procedimiento.query.filter(
								Procedimiento.title == title.data,
								Procedimiento.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:			
			object_already_exist = Procedimiento.query.filter(
							Procedimiento.title == title.data).first() # aqui se presenta la edicion del title de un ITEM registrado
		if object_already_exist:
			raise ValidationError('Ese Título ya existe. Por favor, ingrese uno diferente')
		