from datetime import datetime
from flask import *
from flask_security import current_user, login_required
from flask_wtf import FlaskForm
import logging
import os
import requests
import shutil
import uuid
from werkzeug.exceptions import Forbidden
from wtforms import fields, validators, widgets

from dtech_instagram.InstagramAPI import Instagram

from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import Account, Post

logger = logging.getLogger(__name__)


class PostForm(FlaskForm):
    url = fields.HiddenField("URL")
    image = fields.HiddenField("Image")
    caption = fields.TextAreaField("Caption")
    post_at = fields.DateTimeField("Post at", format='%Y/%m/%d %I:%M %p', validators=[validators.DataRequired()])
    post_at_timezone_offset = fields.IntegerField("Timezone offset", validators=[validators.DataRequired()],
                                                  widget=widgets.HiddenInput())

    def validate(self):
        if not super().validate():
            return False

        result = True

        if not self.url.data and not self.image.data:
            self.url.errors.append("URL or Image must be specified")
            result = False

        return result

    def handle_image(self):
        if self.url.data:
            name = os.path.basename(str(uuid.uuid4()) + os.path.splitext(self.url.data)[1])
            with open(os.path.join(app.config["ROOT_PATH"], "static/uploads", name), "wb") as f:
                r = requests.get(self.url.data, stream=True)
                r.raise_for_status()
                shutil.copyfileobj(r.raw, f)
            return name
        else:
            return self.image.data


@app.route("/upload", methods=("POST",))
@login_required
def upload():
    file = request.files["file"]
    name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(app.config["ROOT_PATH"], "static/uploads", name))
    return jsonify(image=name)


@app.route("/accounts/<int:id>/posts", methods=("GET", "POST"))
@login_required
def account_posts(id):
    account = db.session.query(Account).get(id)
    if account.user != current_user:
        raise Forbidden()

    posts = account.posts
    error = False
    if "scheduled" in request.args:
        posts = posts.filter(Post.posted_at == None)
    elif "posted" in request.args:
        for i in range(5):
            try:
                instagram = Instagram(account.username, account.password, IGDataPath="/tmp/account_%d" % account.id)
                instagram.login()
                posts = []
                for item in instagram.getSelfUserFeed().getItems():
                    post = Post()
                    post.image = item.getImageVersions()[0].getUrl()
                    post.caption = item.getCaption().getText() if item.getCaption() else ""
                    post.posted_at = datetime.fromtimestamp(item.getDeviceTimestamp())
                    posts.append(post)

                break
            except Exception:
                logger.exception("Error retrieving posted posts", exc_info=True)
        else:
            posts = account.posts.filter(Post.posted_at != None)
            error = True
    else:
        return redirect(url_for("account_posts", id=account.id, scheduled="1"))

    return render_template("post/list.html", account=account, error=error, posts=posts)


@app.route("/accounts/<int:account_id>/posts/create", methods=("GET", "POST"))
@login_required
def create_post(account_id):
    account = db.session.query(Account).get(account_id)
    if account.user != current_user:
        raise Forbidden()

    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.account = account
        post.image = form.handle_image()
        post.caption = form.caption.data
        post.post_at = form.post_at.data
        post.post_at_timezone_offset = form.post_at_timezone_offset.data
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("account_posts", id=account.id))

    return render_template("post/create.html", account=account, form=form)


@app.route("/accounts/_/posts/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_post(id):
    post = db.session.query(Post).get(id)
    if post.account.user != current_user:
        raise Forbidden()

    form = PostForm(obj=post)
    if "delete" in request.form:
        account_id = post.account.id
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("account_posts", id=account_id))
    else:
        if form.validate_on_submit():
            post.image = form.handle_image()
            post.caption = form.caption.data
            post.post_at = form.post_at.data
            post.post_at_timezone_offset = form.post_at_timezone_offset.data
            db.session.commit()

            return redirect(url_for("account_posts", id=post.account.id))

        return render_template("post/edit.html", account=post.account, post=post, form=form)
