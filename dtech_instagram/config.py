import os

ROOT_PATH = os.path.dirname(__file__)
SECRET_KEY = os.environ["SECRET_KEY"]

SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = False
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = os.environ["PASSWORD_SALT"]

# Internal services settings

CELERY_BROKER_URL = "amqp://rabbitmq"
CELERYD_HIJACK_ROOT_LOGGER = False

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@postgres/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True

# External services settings

SENTRY_DSN = os.environ.get("SENTRY_DSN")

#
