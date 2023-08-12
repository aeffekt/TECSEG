from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from tseg.models import Equipment, User, Orden_reparacion

class OrdenReparacionForm(FlaskForm):
	def __init__(self, objeto=None):
		super(OrdenReparacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.equipo.choices = [(e.id, e) for e in Equipment.query.all()]
		self.equipo.choices.insert(0,(0, '')) # agrega item "sin datos"
		self.tecnico.choices = [(t.id, t) for t in User.query.filter_by(role_id=3)]
		self.tecnico.choices.insert(0,(0, 'Asignación pendiente')) # agrega item
		self.objeto = objeto

	codigo = StringField('Código', validators=[DataRequired()])
	content = TextAreaField('Descripción', validators=[DataRequired()])
	equipo = SelectField('Equipo', coerce=int, validate_choice=False, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'})
	tecnico = SelectField('Técnico encargado', coerce=int, validate_choice=False)
	submit = SubmitField('Agregar')

	def validate_codigo(self, codigo):
		if ' ' in codigo.data:
			raise ValidationError('El código no puede contener espacios')
		# self.objeto se pasa en UPDATE, no en CREATE, se controla el codigo en objetos de otro ID
		if self.objeto:
			codigo_already_exist = Orden_reparacion.query.filter(
					        Orden_reparacion.codigo == codigo.data,
					        Orden_reparacion.id != self.objeto.id).first()
		else:
			codigo_already_exist = Orden_reparacion.query.filter(
					        Orden_reparacion.codigo == codigo.data).first()
		if codigo_already_exist:
			raise ValidationError('Ese código ya existe. Por favor, ingrese uno diferente')
