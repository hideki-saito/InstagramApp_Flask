from flask import *
from flask_security import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.exceptions import Forbidden
from wtforms import fields, validators

from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import Account


class AccountCreateForm(FlaskForm):
    username = fields.StringField("Username", validators=[validators.DataRequired()])
    password = fields.PasswordField("Password", validators=[validators.DataRequired()])


class AccountEditForm(FlaskForm):
    username = fields.StringField("Username", validators=[validators.DataRequired()])
    password = fields.PasswordField("Password", validators=[validators.DataRequired()])


@app.route("/accounts")
@login_required
def accounts():
    return render_template("account/list.html")


@app.route("/accounts/create", methods=("GET", "POST"))
@login_required
def create_account():
    if len(current_user.accounts) >= current_user.max_accounts:
        return redirect(url_for("index"))

    form = AccountCreateForm()
    if form.validate_on_submit():
        account = Account()
        account.user = current_user
        account.username = form.username.data
        account.password = form.password.data
        db.session.add(account)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("account/create.html", form=form)


@app.route("/accounts/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_account(id):
    account = db.session.query(Account).get(id)
    if account.user != current_user:
        raise Forbidden()

    form = AccountEditForm(obj=account)
    if form.validate_on_submit():
        account.username = form.username.data
        account.password = form.password.data
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("account/edit.html", account=account, form=form)


@app.route("/accounts/<int:id>/delete", methods=("GET", "POST"))
@login_required
def delete_account(id):
    account = db.session.query(Account).get(id)
    if account.user != current_user:
        raise Forbidden()

    db.session.delete(account)
    db.session.commit()
    return redirect(url_for("index"))
