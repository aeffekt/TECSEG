import os
import secrets
from PIL import Image
from flask import url_for,current_app, abort
from flask_login import current_user
from flask_mail import Message
from tseg import mail
from tseg.users.forms import SearchForm
from functools import wraps


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
	output_size = (125,125)
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
			if not current_user.role in roles:
				abort(403)  # Error 403: Acceso prohibido
			return func(*args, **kwargs)
		return wrapper
	return decorator
