from celery import Celery
from celery.schedules import crontab, schedule
from celery.signals import celeryd_after_setup
from flask import has_request_context

from dtech_instagram.app import app
from dtech_instagram.db import db


def make_celery(app, db=None):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            if has_request_context():
                return super(ContextTask, self).__call__(*args, **kwargs)
            else:
                with app.app_context():
                    return super(ContextTask, self).__call__(*args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            if has_request_context():
                pass
            else:
                if db:
                    db.session.remove()

    celery.Task = ContextTask
    return celery


class Cron(object):
    def __init__(self, celery):
        self.celery = celery

        self.jobs = {}

    def job(self, *args, **kwargs):
        def decorator(func):
            celery_task = self.celery.task(**kwargs.pop("params", {}))(func)

            self.celery.conf.CELERYBEAT_SCHEDULE[celery_task.name] = {
                "task":     celery_task.name,
                "schedule": schedule(*args) if args else crontab(**kwargs),
            }

            self.jobs[celery_task.name] = func

            return celery_task

        return decorator


def run_on_startup(task):
    celeryd_after_setup.connect(lambda **kwargs: task.delay(), weak=False)
    return task


celery = make_celery(app, db)
cron = Cron(celery)
