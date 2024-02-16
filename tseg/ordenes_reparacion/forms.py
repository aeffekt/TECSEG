from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from tseg.models import Equipment, User, Orden_reparacion

class OrdenReparacionForm(FlaskForm):
	def __init__(self, objeto=None):
		super(OrdenReparacionForm, self).__init__()  # Llamar al constructor de la clase padre
		self.equipo.choices = [(e.id, e) for e in Equipment.query.all()]
		self.equipo.choices.insert(0,(-1, '')) # agrega item "sin datos"
		self.tecnico.choices = [(t.id, t) for t in User.query.filter_by(role_id=3)]
		self.tecnico.choices.insert(0, (-1, '')) # agrega item
		self.objeto = objeto

	codigo = StringField('Código', validators=[DataRequired()])
	tecnico = SelectField('Técnico encargado', coerce=int, validate_choice=False)
	equipo = SelectField('Equipo', coerce=int, validators=[DataRequired()], render_kw={'data-placeholder': 'Seleccione un item...'})
	content = TextAreaField('Descripción', validators=[DataRequired()])
	materiales = TextAreaField('Materiales')
	horas_trabajadas = StringField('Horas trabajadas')
	submit = SubmitField('Agregar')

	def validate_codigo(self, codigo):
		if not codigo.data.isdigit() or len(codigo.data)!=6:
			raise ValidationError('El código debe contener 6 números.')		
		codigo_mes = int(codigo.data[2:4])
		codigo_dia = int(codigo.data[4:6])
		if not codigo_mes >=1 or not codigo_mes <= 12:
			raise ValidationError('El mes debe ser entre 1 y 12.')
		if not codigo_dia >= 1 or not codigo_dia <= 31:
			raise ValidationError('El dia debe ser entre 1 y 31.')
		# self.objeto se pasa en UPDATE, no en CREATE, se controla el codigo en objetos de otro ID		
		if self.objeto:
			codigo_already_exist = Orden_reparacion.query.filter(
					        Orden_reparacion.codigo == codigo.data,
					        Orden_reparacion.id != self.objeto.id).first() # al cambiar el ID significa que es un nuevo ITEM
		else:
			codigo_already_exist = Orden_reparacion.query.filter(
					        Orden_reparacion.codigo == codigo.data).first() # aqui se presenta la edicion del Codigo de un ITEM registrado
		if codigo_already_exist:
			raise ValidationError('Ese código ya existe. Por favor, ingrese uno diferente')
