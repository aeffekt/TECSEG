from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg import db
from tseg.models import Pais, Provincia

class ClientForm(FlaskForm):
	def __init__(self):
		super(ClientForm, self).__init__()  # Llamar al constructor de la clase padre
		self.pais.choices = [(p.id, p.nombre) for p in Pais.query.all()]  # Cargar opciones de países
		self.pais.choices.append([0,"Otro"]) # agrega item "Otro"

	client_name = StringField('Nombre', validators=[DataRequired()], render_kw={'autofocus': True})
	business_name = StringField('Razón social')
	contact = StringField('Contacto', validators=[DataRequired()])
	comments = TextAreaField('Comentarios')
	direccion = StringField('Domicilio completo')
	pais = SelectField('Pais', coerce=str, validate_choice=False)
	provincia = StringField('Provincia')
	ciudad = StringField('Ciudad')
	codigo_postal = StringField('Código Postal')
	submit = SubmitField('Agregar')