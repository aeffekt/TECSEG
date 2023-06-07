from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class OrdenReparacionForm(FlaskForm):
	codigo = StringField('Código', validators=[DataRequired()])
	content = TextAreaField('Descripción')
	equipment = SelectField('Equipment', choices=[], coerce=str, validate_choice=False, validators=[DataRequired()])
	submit = SubmitField('Agregar')
