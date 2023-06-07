from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Eq_detailForm(FlaskForm):
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Historia', validators=[DataRequired()])
	submit = SubmitField('Aceptar')
