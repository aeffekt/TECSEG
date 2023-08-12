from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class MarcaForm(FlaskForm):	
	nombre = StringField('Nombre', validators=[DataRequired()])		
	submit = SubmitField('Crear / Actualizar')