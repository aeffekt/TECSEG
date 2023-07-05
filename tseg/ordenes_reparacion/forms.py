from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Equipment, User, Estado_or

class OrdenReparacionForm(FlaskForm):
	def __init__(self):
		super(OrdenReparacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.equipo.choices = [e for e in Equipment.query.all()]
		self.tecnico.choices = [t for t in User.query.filter_by(role_id=3)]
		self.tecnico.choices.insert(0,'Asignación pendiente') # agrega item		

	codigo = StringField('Código *', validators=[DataRequired()])
	content = TextAreaField('Descripción *', validators=[DataRequired()])
	equipo = SelectField('Equipo', coerce=str, validate_choice=False, validators=[DataRequired()])
	tecnico = SelectField('Técnico encargado', coerce=str, validate_choice=False)
	submit = SubmitField('Agregar')
