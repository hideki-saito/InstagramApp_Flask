from flask_security import Security, SQLAlchemyUserDatastore

from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
