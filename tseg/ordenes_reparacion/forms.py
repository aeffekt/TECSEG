from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from tseg.models import Equipment, User, Estado_or

class OrdenReparacionForm(FlaskForm):
	def __init__(self):
		super(OrdenReparacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.equipo.choices = [f'[{e.id}] {e.title} ({e.owner.nombre} {e.owner.apellido})' for e in Equipment.query.all()]
		self.tecnico.choices = [f'[{t.id}] {t.username} ({t.role.role_name})' for t in User.query.filter_by(role_id=3)]
		self.tecnico.choices.insert(0,'Asignación pendiente') # agrega item
		self.estado.choices = [f'[{estado_or.id}] {estado_or.descripcion}' for estado_or in Estado_or.query.all()]

	codigo = StringField('Código (*)', validators=[DataRequired()])
	content = TextAreaField('Descripción')
	equipo = SelectField('Equipo', coerce=str, validate_choice=False, validators=[DataRequired()])
	tecnico = SelectField('Técnico encargado', coerce=str, validate_choice=False)
	estado = SelectField('Estado', coerce=str, validate_choice=False)
	submit = SubmitField('Agregar')
