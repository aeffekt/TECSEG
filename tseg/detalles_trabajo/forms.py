from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, TextAreaField, IntegerField

class DetalleTrabajoForm(FlaskForm):	
	content = TextAreaField('Detalle Item Orden de Trabajo', validators=[DataRequired()])
	cantidad = IntegerField('Cantidad', default=1, validators=[DataRequired(), NumberRange(min=1)])
	submit = SubmitField('Aceptar')
