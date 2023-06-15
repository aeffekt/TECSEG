import os


class Config:	
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True # SECURITY 
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.getenv('EMAIL_USER') #setear variable de entorno en S.O. servidor
	MAIL_PASSWORD = os.getenv('EMAIL_PASS') #IDEM, y reiniciar el sistema
	MAIL_DEBUG = True
	MAIL_DEFALUT_SENDER = None
	MAIL_MAX_EMAILS = 15
	MAIL_ASCII_ATTACHMENTS = False
	PER_PAGE=10