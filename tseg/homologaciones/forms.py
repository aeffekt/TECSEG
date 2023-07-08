from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class HomologacionForm(FlaskForm):
	modelo = StringField('modelo', validators=[DataRequired()])
	codigo = StringField('Código', validators=[DataRequired()])	
	submit = SubmitField('Crear / Actualizar')

	def validate_codigo(self, codigo):
		if ' ' in codigo.data:
			raise ValidationError('El código puede contener espacios')
