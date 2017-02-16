from flask import *

from dtech_instagram.app import app


@app.route("/")
def index():
    return redirect("accounts")
