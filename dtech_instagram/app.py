from flask import Flask
import logging

import dtech_instagram.config

logger = logging.getLogger(__name__)

__all__ = ["app"]

app = Flask("dtech_instagram")
app.config.from_object(dtech_instagram.config)
app.url_map.strict_slashes = False
