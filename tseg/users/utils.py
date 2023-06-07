import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from tseg import mail


def save_picture(form_picture):
	random_hex = secrets.token_hex(8) #crea nombre random para la imagen elegida
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext #conserva la extension original del archivo
	picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)
	# resize image
	print(picture_path)
	output_size = (125,125)
	i = Image.open(form_picture)
	i_rgb = i.convert('RGB') # si es png o tiene trnassparencia se la quito asi evita errores
	i_rgb.thumbnail(output_size)
	i_rgb.save(picture_path)

	return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('TECSEG - Reset de contraseña requerido',
                  sender='no-reply@tec-seg.com',
                  recipients=[user.email])
    msg.body = f'''Usuario: {user.username} \n Para resetear su contraseña use el siguiente link:
{url_for('users.reset_token', token=token, _external=True)}

Si ud no hizo este requerimiento, ignore este mensaje.'''
    mail.send(msg)