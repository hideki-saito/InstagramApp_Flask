from setuptools import setup, find_packages


setup(
    name="dtech_instagram",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "alembic",
        "celery",
        "Flask",
        "Flask-Bootstrap",
        "Flask-Security",
        "Flask-SQLAlchemy",
        "Pillow",
        "psycopg2",
        "raven[flask]",
        "requests",
    ],
)
