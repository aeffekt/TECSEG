from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Tipologia
from tseg import db

class HistoriaForm(FlaskForm):
	def __init__(self):
		super(HistoriaForm, self).__init__()  # Llamar al constructor de la clase padre
		self.tipo.choices = [tipo for tipo in Tipologia.query.order_by(Tipologia.id).all()]

	tipo = SelectField('Tipo de historia', coerce=str, validate_choice=False, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'})
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Historia')
	submit = SubmitField('Aceptar')
