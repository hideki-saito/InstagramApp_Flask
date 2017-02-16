import codecs
import logging
from raven.contrib.flask import Sentry
import sys
from werkzeug.exceptions import HTTPException

from dtech_instagram.app import app
from dtech_instagram.celery import celery
from dtech_instagram.db import db
from dtech_instagram.models import *

import dtech_instagram.admin
import dtech_instagram.bootstrap
import dtech_instagram.mail
import dtech_instagram.security
import dtech_instagram.worker
import dtech_instagram.views

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s",
                    stream=codecs.getwriter("utf-8")(sys.stdout.buffer, "replace") if hasattr(sys.stdout, "buffer") else None)
logging.getLogger("amqp").setLevel(logging.WARNING)
logging.getLogger("celery").setLevel(logging.INFO)
logging.getLogger("celery.redirected").setLevel(logging.ERROR)
logging.getLogger("kombu").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

if app.config.get("SENTRY_DSN"):
    app.config["RAVEN_IGNORE_EXCEPTIONS"] = [HTTPException]
    sentry = Sentry(app)
