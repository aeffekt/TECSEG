from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import SubmitField, TextAreaField, IntegerField

class DetalleTrabajoForm(FlaskForm):	
	content = TextAreaField('Detalle Item Orden de Trabajo', validators=[DataRequired()])
	cantidad = IntegerField('Cantidad', default=1)
	submit = SubmitField('Aceptar')
