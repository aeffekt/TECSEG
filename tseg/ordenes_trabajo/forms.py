import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from tseg.models import Client, Orden_trabajo, Estado_ot

class OrdenTrabajoForm(FlaskForm):
	def __init__(self, objeto=None):
		super(OrdenTrabajoForm, self).__init__()  # Llamar al constructor de la clase padre		
		self.client.choices = [(c.id, c) for c in Client.query.filter_by()]
		self.client.choices.insert(0,(0, '')) # agrega item
		self.estado.choices = [(e.id, e) for e in Estado_ot.query.filter_by()]		
		self.objeto = objeto

	codigo = StringField('Código', validators=[DataRequired()])
	content = TextAreaField('Descripción')	
	client = SelectField('Cliente', coerce=int, validators=[DataRequired(message='Debe seleccionar un cliente')], render_kw={'data-placeholder': 'Seleccione un item...'})
	estado = SelectField('Estado', coerce=int)
	submit = SubmitField('Agregar')

	def validate_codigo(self, codigo):
		if not codigo.data.isdigit() or len(codigo.data) !=6:
			raise ValidationError('El código debe contener 6 números.')		
		codigo_mes = int(codigo.data[2:4])
		codigo_dia = int(codigo.data[4:6])
		if not codigo_mes >=1 or not codigo_mes <= 12:
			raise ValidationError('El mes debe ser entre 1 y 12.')
		if not codigo_dia >= 1 or not codigo_dia <= 31:
			raise ValidationError('El dia debe ser entre 1 y 31.')
		if self.objeto:
			# self.objeto se pasa en UPDATE se controla el codigo en objetos de otro ID		
			codigo_already_exist = Orden_trabajo.query.filter(
					        Orden_trabajo.codigo == codigo.data,
					        Orden_trabajo.id != self.objeto.id).first()
		else:
			codigo_already_exist = Orden_trabajo.query.filter(
					        Orden_trabajo.codigo == codigo.data).first()
		if codigo_already_exist:
			raise ValidationError('Ese código ya existe. Por favor, ingrese uno diferente')
