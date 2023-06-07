from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	content = TextAreaField('Mensaje', validators=[DataRequired()])
	submit = SubmitField('Publicar')
