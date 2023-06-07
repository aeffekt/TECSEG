from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class EquipmentForm(FlaskForm):
	title = StringField('Nombre', validators=[DataRequired()])
	content = TextAreaField('Descripción')
	owner = SelectField('Cliente', choices=[], coerce=str, validate_choice=False, validators=[DataRequired()])
	submit = SubmitField('Agregar')