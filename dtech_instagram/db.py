import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import Column

from dtech_instagram.app import app

logger = logging.getLogger(__name__)

__all__ = ["db"]


class NotNullableColumn(Column):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("nullable", False)
        super().__init__(*args, **kwargs)


db = SQLAlchemy(app)
db.Column = NotNullableColumn
db.Model.get_default = lambda self, column_name: getattr(self.__class__, column_name).default.execute(db.session.bind)
db.Model.__repr__ = lambda self: "<%s id=%s>" % (self.__class__.__name__, self.id or "0x%x" % id(self))
