import os, re
import secrets
from PIL import Image
from flask import url_for,current_app, abort
from flask_login import current_user
from flask_mail import Message
from tseg import mail
from tseg.users.forms import SearchForm
from functools import wraps
from datetime import datetime
from tseg.models import Ciudad, Provincia, Pais


# obtener_informacion_geografica
def obtener_informacion_geografica(codigo_postal):	
	ciudad_nombre = ''
	provincia_nombre = ''
	pais_nombre = ''
	ciudad = Ciudad.query.filter_by(cp=codigo_postal).first()
	if ciudad:
		provincia = Provincia.query.filter(Provincia.id==ciudad.provincia_id).first()
		pais = Pais.query.filter(Pais.id==provincia.pais_id).first()
		ciudad_nombre = ciudad.nombre
		provincia_nombre = provincia.nombre
		pais_nombre = pais.nombre

	return ciudad_nombre, provincia_nombre, pais_nombre;
		


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
