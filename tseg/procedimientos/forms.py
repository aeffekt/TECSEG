from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ProcedimientoForm(FlaskForm):
	
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Procedimiento')
	submit = SubmitField('Aceptar')
