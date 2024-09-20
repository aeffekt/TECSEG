TECSEG Tecnología & Seguridad - Agustin Arnaiz 2023

SETUP PYTHON 3.8.10

CMD: 
pip install -r requerimientos.txt --yes

pip install mysql-connector
pip install mysql-connector-python
pip install pymysql
pip install flask
pip install flask_wtf
pip install flask-sqlalchemy
pip install flask-Bcrypt
pip install flask-login
pip install flask-mail
pip install itsdangerous==2.0.1
pip install email_validator
pip install pillow (image)
pip install requests
pip install reportlab
pip install qrcode

pip install wfastcgi
wfastcgi-enable

Bootstrap
select2
Chart.js


PYTHON:
import secrets:
secrets.token_hex(16): #16  bytes --> resultado se como codigo de seguridad

DATABASE:
CMD:
python
>>> from tseg import db
>>> db.create_all()
>>> User.query.all()
[]

SECURITY:
CMD:
python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> hashed_pw = bcrypt.generate_password_hash('admin')
>>> bcrypt.check_password_hash(hashed_pw, 'password') = False
>>> bcrypt.check_password_hash(hashed_pw, 'admin') = True

SHELL_VARIABLES (RESTART O.S. AFTER EDIT):
SECRET_KEY
SQLALCHEMY_DATABASE_URI (sqlite:///db.db) (usar ruta absoluta si no encuentra db)
EMAIL_USER
EMAIL_PASS

NOTE: datetime.datetime fromisoformat requiere Python 3.7 o superior

usar servidor debug (no requiere reiniciar al actualizar)
CMD: DIR/set FLASK_DEBUG=1
CMD: python run.py
Browser: "localhost:5000"


Versión: 0.0.1

29/09/21 (Token que expira en segundos)
>> python
>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
>> s = Serializer('secret', 30) #time 30secs
>> token = s.dumps({'user_id': 1}.decode('utf-8'))
>> token