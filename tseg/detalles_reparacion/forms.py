from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField

class DetalleReparacionForm(FlaskForm):	
	content = TextAreaField('Detalle Reparación')
	submit = SubmitField('Aceptar')
