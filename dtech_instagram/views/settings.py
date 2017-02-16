from flask import *
from flask_security import current_user, login_required
from flask_security.utils import encrypt_password
from flask_wtf import FlaskForm
from wtforms import fields, validators

from dtech_instagram.app import app
from dtech_instagram.db import db


class SettingsForm(FlaskForm):
    password = fields.PasswordField("Password",
                                    validators=[validators.EqualTo("password_confirm",
                                                                   "Passwords must match")])
    password_confirm = fields.PasswordField("Password confirm")


@app.route("/settings", methods=("GET", "POST"))
@login_required
def settings():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        if form.password.data:
            current_user.password = encrypt_password(form.password.data)
        db.session.commit()

        return redirect(url_for("settings"))

    return render_template("settings.html", form=form)
