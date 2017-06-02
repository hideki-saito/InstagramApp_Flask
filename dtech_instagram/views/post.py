from datetime import datetime, timedelta

import logging
import os
import requests
import shutil
import uuid
import re

from flask import *
from flask_security import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.exceptions import Forbidden
from wtforms import fields, validators, widgets
from sqlalchemy import desc

from dtech_instagram.InstagramAPI import Instagram
from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import Account, Post, Folder, Image, Ins_Profile, Ins_Posted, Ins_History
from dtech_instagram.views import ajax

logger = logging.getLogger(__name__)


class PostForm(FlaskForm):
    url = fields.HiddenField("URL")
    image = fields.HiddenField("Image")
    caption = fields.TextAreaField("Caption")
    post_at = fields.DateTimeField("Post at", format='%m/%d/%Y %I:%M %p', validators=[validators.DataRequired()])
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
            return ajax.save_file(self.url.data)

        else:
            return self.image.data


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route("/upload", methods=("POST",))
@login_required
def upload():
    file = request.files["file"]
    name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(app.config["ROOT_PATH"], "static/uploads", name))
    return jsonify(image=name)

@app.route("/accounts/<int:account_id>/analytics/follow_back", methods=("GET", "POST"))
@login_required
def follow_back(account_id):
    account = db.session.query(Account).get(account_id)
    instagram = Instagram(account.username, account.password, IGDataPath="/tmp/account_%s" % account.username)

    return render_template("analytics/follow_back.html", account=account, profile=instagram.getProfileData())

@app.route("/accounts/<int:account_id>/analytics/unfollowers", methods=("GET", "POST"))
@login_required
def unfollowers(account_id):
    account = db.session.query(Account).get(account_id)
    instagram = Instagram(account.username, account.password, IGDataPath="/tmp/account_%s" % account.username)

    return render_template("analytics/unfollowers.html", account=account, profile=instagram.getProfileData())


@app.route("/accounts/<int:account_id>/analytics/followers", methods=("GET", "POST"))
@login_required
def followers(account_id):
    account = db.session.query(Account).get(account_id)
    instagram = Instagram(account.username, account.password, IGDataPath="/tmp/account_%s" % account.username)

    return render_template("analytics/followers.html", account=account, profile=instagram.getProfileData())


@app.route("/accounts/<int:account_id>/analytics/dashboard", methods=("GET", "POST"))
@login_required
def dashboard(account_id):
    account = db.session.query(Account).get(account_id)
    if account.user != current_user:
        raise Forbidden()

    try:
        profile = account.ins_profile
        history_info = account.ins_history
        now_info = history_info[0]
        now_date = now_info.history_at
        a_month_before = (now_date - timedelta(days=30)).date()
        try:
            compared_info = history_info.filter(a_month_before < Ins_History.history_at)[-1]
        except:
            compared_info = history_info[-1]

        followers_count_difference = now_info.followers_count - compared_info.followers_count
        followings_count_difference = now_info.followings_count - compared_info.followings_count
        posts_count_difference = now_info.posts_count - compared_info.posts_count
        likes_count_difference = now_info.likes_count - compared_info.likes_count
        comments_count_difference = now_info.comments_count - compared_info.comments_count
        difference_info = {'followers_count': followers_count_difference,
                           'followings_count': followings_count_difference,
                           'posts_count': posts_count_difference,
                           'likes_count': likes_count_difference,
                           'comments_count': comments_count_difference}

        account_posts = account.ins_posts
        recent_posts = account_posts[0:7]
        recent_avarage_likes_count = int(sum([item.likes_count for item in recent_posts]) / len(recent_posts))
        recent_avarage_comments_count = int(sum([item.comments_count for item in recent_posts]) / len(recent_posts))

        recent_likes_chart_data = []
        recent_comments_chart_data = []
        for post in recent_posts:
            item1 = {}
            item1['img_url'] = re.match(r".+\.jpg\?", post.thum_url).group()[:-1]
            item1['label'] = ""
            item1['value'] = post.likes_count
            recent_likes_chart_data.append(item1)

            item2 = {}
            item2['img_url'] = re.match(r".+\.jpg\?", post.thum_url).group()[:-1]
            item2['label'] = ""
            item2['value'] = post.comments_count
            recent_comments_chart_data.append(item2)

        recent_info = {'posts': recent_posts,
                       'avarage_likes_count': recent_avarage_likes_count,
                       'average_comments_count': recent_avarage_comments_count,
                       'likes_chart_data': json.dumps(recent_likes_chart_data),
                       'comments_chart_data': json.dumps(recent_comments_chart_data)
                       }


        top_liked_posts = db.session.query(Ins_Posted).filter(
            Ins_Posted.account_id==account_id).order_by(desc(Ins_Posted.likes_count))[0:3]

        top_commented_posts = db.session.query(Ins_Posted).filter(
            Ins_Posted.account_id == account_id).order_by(desc(Ins_Posted.comments_count))[0:3]


        return render_template(
            "analytics/dashboard.html",
            profile=profile,
            account=account,
            now_info=now_info,
            difference_info=difference_info,
            recent_info=recent_info,
            top_liked_posts=top_liked_posts,
            top_commented_posts=top_commented_posts
        )

    except Exception as ex:
        print (ex)
        return render_template("analytics/wait.html", account=account)

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
        return render_template("post/list.html", account=account, error=error, posts=posts)

    elif "posted" in request.args:
        profile = account.ins_profile
        now_info = account.ins_history[0]
        posts = account.ins_posts

        return render_template(
            "post/posted.html", profile=profile, now_info=now_info, account=account, error=error, posts=posts
        )

        # return render_template('post/posted.html', account=account)
    else:
        return redirect(url_for("account_posts", id=account.id, scheduled="1"))


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

    images = {}
    folders = current_user.folders
    for folder in folders:
        images[folder] = folder.images

    # images = Image.query.all()
    # images = folders[0].images
    return render_template("post/create.html", account=account, form=form, images=images)


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


@app.route("/swap-posts", methods=("POST",))
@login_required
def swap_posts():
    post_1 = db.session.query(Post).get(request.form["id_1"])
    if post_1.account.user != current_user:
        raise Forbidden()

    post_2 = db.session.query(Post).get(request.form["id_2"])
    if post_2.account.user != current_user:
        raise Forbidden()

    post_1.image, post_2.image = post_2.image, post_1.image
    post_1.caption, post_2.caption = post_2.caption, post_1.caption
    db.session.commit()

    return jsonify({})

