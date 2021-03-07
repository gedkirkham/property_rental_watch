import os

class AllowedHosts:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

class Database:
    NAME = os.environ.get('POSTGRES_DB')
    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    HOST = os.environ.get('POSTGRES_HOST')
    PORT = os.environ.get('POSTGRES_PORT')

class Debug:
    DEBUG = os.environ.get('DEBUG', 0)

class Email:
    ADDRESS = os.environ.get('EMAIL_ADDRESS')
    BACKEND = os.environ.get('EMAIL_BACKEND')
    HOST = os.environ.get('EMAIL_HOST')
    PASSWORD = os.environ.get('EMAIL_PASSWORD')
    PORT = os.environ.get('EMAIL_PORT')

class Secrets:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')