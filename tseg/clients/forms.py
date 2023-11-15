from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional, Email, NumberRange
from tseg.models import Cond_fiscal, Iibb, Pais, Client

class ClientForm(FlaskForm):
	def __init__(self, objeto=None):
		super(ClientForm, self).__init__()  # Llamar al constructor de la clase padre		
		self.cond_fiscal.choices = [(cond_fiscal.id, cond_fiscal.nombre) for cond_fiscal in Cond_fiscal.query.all()]
		self.iibb.choices = [(iibb.jurisdiccion, iibb) for iibb in Iibb.query.order_by(Iibb.jurisdiccion.asc()).all()]
		self.pais.choices = [p for p in Pais.query.all()]
		self.pais.choices.insert(0,'') # agrega item "sin datos"
		self.objeto = objeto

	nombre = StringField('Nombre', validators=[DataRequired()], render_kw={'autofocus': True})
	apellido = StringField('Apellido', validators=[DataRequired()])
	business_name = StringField('Razón social')
	email = StringField('Email', validators=[Optional(), Email()])
	telefono = StringField('Teléfono')
	comments = TextAreaField('Comentarios')

	direccion = StringField('Dirección (Calle y número)')
	codigo_postal = IntegerField('Código Postal', validators=[Optional(), NumberRange(min=1000, max=9999)])
	localidad = StringField('Localidad')
	provincia = StringField('Provincia')	
	pais = SelectField('Pais', coerce=str, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})

	cuit = IntegerField('CUIT', validators=[Optional(), NumberRange(min= 20000000000, max=33999999999)])
	cond_fiscal = SelectField('Condición fiscal', coerce=int, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})
	iibb = SelectField('Ingresos brutos', coerce=int, validate_choice=False, render_kw={'data-placeholder': 'Seleccione un item...'})
		
	submit = SubmitField('Agregar/Actualizar')

	# validacion del nombre+apellido
	def validate_nombre(self, field):		
		if self.objeto:
			client_already_exist = Client.query.filter(
					        Client.nombre == self.nombre.data,
							Client.apellido == self.apellido.data,
					        Client.id != self.objeto.id).first()
		else:
			client_already_exist = Client.query.filter(
					        Client.nombre == self.nombre.data,
							Client.apellido == self.apellido.data).first()
		if client_already_exist:
			raise ValidationError('Ya existe un cliente con el mismo nombre y apellido')
		
	
	# validacion del nombre+apellido
	def validate_business_name(self, business_name):		
		if business_name.data != '' and business_name.data !=None:
			if self.objeto:
				business_already_exist = Client.query.filter(
								Client.business_name == business_name.data,
								Client.id != self.objeto.id).first()
			else:			
				business_already_exist = Client.query.filter(					        
								Client.business_name == business_name.data).first()
			if business_already_exist:
				raise ValidationError('Ya existe un cliente con el mismo nombre de negocio')
		
	# Validación de domicilio, código postal, país, provincia y localidad
	def validate_direccion(self, field):		
		# Verifica si al menos uno de los campos está lleno
		if any([self.codigo_postal.data, self.localidad.data, self.provincia.data, self.pais.data, self.direccion.data]):
			if not all([self.codigo_postal.data, self.localidad.data, self.provincia.data, self.pais.data, self.direccion.data]):
				flash("Advertencia! Debe completar: Código Postal, Dirección, Localidad, Provincia y Pais del domicilio, o ninguno de esos datos.", 'warning')
				raise ValidationError('Completar el resto de los campos de domicilio.')
