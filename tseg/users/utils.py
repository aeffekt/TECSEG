import os, re
import secrets
from PIL import Image
from flask import url_for,current_app, abort, request
from flask_login import current_user
from flask_mail import Message
from tseg import mail
from functools import wraps
from datetime import datetime
from tseg.models import Equipment, Client, User, Historia, Orden_reparacion, Localidad, Provincia, Pais, Tipologia
from sqlalchemy import asc, desc


# obtener el nombre del atributo para filtrar la búsqueda
def buscarLista(dBModel, *arg):
	order_by = dBModel.__table__.columns.keys()[0]
	select_item = request.args.get('selectItem', '')
	# Obtener los valores de filterBy y filterOrder desde la solicitud
	if not select_item:
		# sino hay un elemento seleccionado, carga orden por parametro
		order_by = request.args.get('orderBy', order_by)
	order_order = request.args.get('orderOrder', 'desc')
	sort_column = getattr(dBModel, order_by)

	# ORDEN	
	if order_order == "asc":
		orden = asc(sort_column)
	else:
		orden = desc(sort_column)

	lista = dBModel.query.order_by(orden)	
	if arg:

		# filtrado extra de O.R.
		if dBModel==Orden_reparacion:
			# ordenes de reparacion por tecnico
			if isinstance(arg[0], User):
				lista = lista.filter_by(tecnico_id=arg[0].id)

			# ordenes de reparacion por equipo
			if isinstance(arg[0], Equipment):
				lista = lista.filter_by(equipo_id=arg[0].id)
		
		# filtrado extra Historias 
		elif dBModel==Historia:

			# para un equipo determinado
			if isinstance(arg[0], Equipment):
				lista = lista.filter_by(equipo_id=arg[0].id)
				if len(arg)==2:
					lista.filter_by(tipologia_id=arg[1])

			# para un usuario determinado
			if isinstance(arg[0], User):
				print(arg)
				print(arg[0])
				lista = lista.filter_by(author_historia=arg[0])
	return lista
	

# obtener_informacion_geografica
def obtener_informacion_geografica(codigo_postal):	
	localidad_nombre = ''
	provincia_nombre = ''
	pais_nombre = ''
	localidad = Localidad.query.filter_by(cp=codigo_postal).first()
	if localidad:
		provincia = Provincia.query.filter(Provincia.id==localidad.provincia_id).first()
		pais = Pais.query.filter(Pais.id==provincia.pais_id).first()
		localidad_nombre = localidad.nombre
		provincia_nombre = provincia.nombre
		pais_nombre = pais.nombre

	return localidad_nombre, provincia_nombre, pais_nombre;


def dateFormat():
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	return datetime.fromisoformat(now)

# extrae datos dentro de corchetes
def identificador_en_corchete(cadena):
	patron = r"\[([^]]+)\]"
	cadena_en_patron = re.findall(patron, cadena)  # busca el id dentro de corchetes	
	if cadena_en_patron:
		return cadena_en_patron[0]
	return None


def save_picture(form_picture, folder):
	img = Image.open(form_picture)
	
	random_hex = secrets.token_hex(8) #crea nombre random para la imagen elegida
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext #conserva la extension original del archivo
	picture_path = os.path.join(current_app.root_path, f'static\\{folder}', picture_fn)

	# se toma el ancho y alto de la imagen
	width, height = img.size
	top = 0
	bottom = height
	left = 0
	right = width

	if width > height:		
		diff = (width - height)/2
		left = diff
		right = width - diff
	elif height > width:
		diff = (height - width)/2
		top = diff
		bottom = height - diff
	output_size = (right-left,bottom-top)
	img_cropped = img.crop((left, top, right, bottom))
	
	img_rgb = img_cropped.convert('RGB') # si es png o tiene trnassparencia se la quito asi evita errores
	img_rgb.thumbnail(output_size)
	img_rgb.save(picture_path)

	return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('TECSEG - Reset de contraseña requerido',
                  sender='no-reply@tecseg.local',
                  recipients=[user.email])
    msg.body = f'''Usuario: {user.username} \n Para resetear su contraseña use el siguiente link:
{url_for('users.reset_token', token=token, _external=True)}

Si ud no hizo este requerimiento, ignore este mensaje.'''
    mail.send(msg)


def role_required(*roles):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if not current_user.role.role_name in roles:
				abort(403)  # Error 403: Acceso prohibido
			return func(*args, **kwargs)
		return wrapper
	return decorator
