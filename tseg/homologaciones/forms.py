from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Modelo

class HomologacionForm(FlaskForm):
	def __init__(self):
		super(HomologacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.modelo.choices = [modelo.nombre for modelo in Modelo.query.all() if modelo.homologacion_id is None]

	modelo = SelectField('Modelo',coerce=str, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'})
	codigo = StringField('Código', validators=[DataRequired()])	
	submit = SubmitField('Crear / Actualizar')

	def validate_codigo(self, codigo):
		if ' ' in codigo.data:
			raise ValidationError('El código puede contener espacios')
