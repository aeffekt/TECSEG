import os, re
import secrets
from PIL import Image
from flask import url_for,current_app, abort, request
from flask_login import current_user
from flask_mail import Message
from tseg import mail
from tseg.users.forms import SearchForm
from functools import wraps
from datetime import datetime
from tseg.models import Equipment, Client, User, Historia, Orden_reparacion, Localidad, Provincia, Pais
from sqlalchemy import asc, desc


# obtener el nombre del atributo para filtrar la búsqueda
def buscarLista(dBModel, *arg):
	# Obtener los valores de filterBy y filterOrder desde la solicitud
	filter_by = request.args.get('filterBy')	
	sort_column = getattr(dBModel, filter_by)

	# ORDEN
	filter_order = request.args.get('filterOrder')
	if filter_order == "asc":
		orden = asc(sort_column)
	else:
		orden = desc(sort_column)

	lista = dBModel.query.order_by(orden)
	if arg:
		# filtrar busqueda de O.R. si la hace un tecnico
		if isinstance(arg[0], User):			
			lista = lista.filter_by(tecnico_id=arg[0].id)
		# filtrar busqueda de Historias para un equipo determinado
		elif isinstance(arg[0], Equipment):			
			lista = lista.filter_by(equipo_id=arg[0].id)
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

def extraerId(cadena):
	patron = r"\[(\d+)\]"
	id_extraido_list = re.findall(patron, cadena) #busca el id dentro de corchetes
	if id_extraido_list:
		return id_extraido_list[0]
	return None


def save_picture(form_picture):
	random_hex = secrets.token_hex(8) #crea nombre random para la imagen elegida
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext #conserva la extension original del archivo
	picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)
	# resize image	
	
	i = Image.open(form_picture)
	width, height = i.size
	desired_width = 125  # Ancho deseado en píxeles
	desired_height = 125  # Alto deseado en píxeles
	left = (width - desired_width) // 2
	top = (height - desired_height) // 2
	right = (width + desired_width) // 2
	bottom = (height + desired_height) // 2
	i_cropped = i.crop((left, top, right, bottom))

	i_rgb = i.convert('RGB') # si es png o tiene trnassparencia se la quito asi evita errores
	output_size = (desired_width,desired_height)
	i_rgb.thumbnail(output_size)
	i_rgb.save(picture_path)

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
