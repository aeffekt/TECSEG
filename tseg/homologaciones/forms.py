from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HomologacionForm(FlaskForm):
	modelo = StringField('modelo', validators=[DataRequired()])
	codigo = StringField('Código', validators=[DataRequired()])	
	submit = SubmitField('Crear / Actualizar')
