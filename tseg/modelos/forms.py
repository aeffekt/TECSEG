from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from datetime import datetime

class ModeloForm(FlaskForm):
	def __init__(self):
		super(ModeloForm, self).__init__()  # Llamar al constructor de la clase padre
		self.anio.choices = [f"'{str(year)[2:]}" for year in range(datetime.now().year + 1, 1999, -1)]
		self.anio.choices.insert(0,'N/D')

	nombre = StringField('Nombre', validators=[DataRequired()])
	anio = SelectField('Año del modelo',coerce=str, validators=[DataRequired()])
	descripcion = TextAreaField('Descripción')
	picture = FileField('Imagen de equipo', validators=[FileAllowed(['jpg', 'png', 'bmp', 'gif'])])
	submit = SubmitField('Crear / Actualizar')