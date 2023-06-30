from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class ModeloForm(FlaskForm):
	nombre = StringField('Nombre', validators=[DataRequired()])
	descripcion = TextAreaField('Descripción')
	picture = FileField('Imagen de equipo', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif'])])
	submit = SubmitField('Crear / Actualizar')