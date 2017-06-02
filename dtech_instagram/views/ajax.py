import os
import re
import shutil
import uuid
import json
import base64
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import *
from flask_security import current_user

from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import Account, Post, Folder, Image
from dtech_instagram.InstagramAPI import Instagram

def save_file(original_uri):
    uri = str(uuid.uuid4()) + ".jpeg"
    with open(os.path.join(app.config["ROOT_PATH"], "static/uploads", uri), "wb") as f:
        if 'base64' in original_uri:
            img_data = re.search(r"base64.+", original_uri).group().replace("base64,", '')
            f.write(base64.b64decode(img_data))
        else:
            r = requests.get(original_uri, stream=True)
            r.raise_for_status()
            shutil.copyfileobj(r.raw, f)

        return uri


@app.route('/save_image', methods=['GET','POST'])
def save_image():
    global selected
    name = request.args.get('name', '', type=str)
    folder = request.args.get('folder', '', type=str)
    data = request.args.get('data', '', type=str)
    # id = request.args.get('id', '', type=str)

    soup = BeautifulSoup(data, 'html.parser')
    original_uri = soup.find('img').get('src')
    new_uri = save_file(original_uri)

    image = Image()
    image.folder_id = folder.split('-')[1]
    image.name = name
    image.uri = new_uri
    db.session.add(image)
    db.session.commit()

    return json.dumps({'uri': new_uri})


@app.route('/upload_images', methods=['POST'])
def upload_images():
    if request.method == 'POST':
        uploaded_images = request.files.getlist("file[]")
        folder_id = request.form.get('folder_id')

        uploaded_image_names = []
        uploaded_image_uris = []
        for uploaded_image in uploaded_images:
            uri = ".".join([str(uuid.uuid4()), uploaded_image.filename.split(".")[1]])
            uploaded_image.save(os.path.join(app.config["ROOT_PATH"], "static/uploads", uri))
            uploaded_image_uris.append(uri)
            uploaded_image_names.append(uploaded_image.filename)
            image = Image()
            image.folder_id = folder_id.split('-')[1]
            image.name = uploaded_image.filename
            image.uri = uri
            db.session.add(image)
            db.session.commit()

        return jsonify(uris=uploaded_image_uris, names=uploaded_image_names)


@app.route('/create_folder', methods=['GET','POST'])
def create_folder():
    global selected
    name = request.args.get('name', '', type=str)

    folder = Folder()
    folder.user_id = current_user.id
    folder.name = name

    db.session.add(folder)
    db.session.commit()

    return json.dumps({'folder_id': folder.id})


@app.route('/rename', methods=['GET','POST'])
def rename():
    global selected
    id = request.args.get('id', '', type=str)
    new_name = request.args.get('new_name', '', type=str)
    type = request.args.get('type', '', type=str)

    if type == 'folder':
        id = id.split("-")[1]
        folder = db.session.query(Folder).get(id)
        folder.name = new_name
        db.session.commit()

        return json.dumps({'result': 'success'})

    else:
        image = Image.query.filter_by(uri=id).first()
        image.name = new_name
        db.session.commit()

        return json.dumps({'result': 'success'})


@app.route('/delete', methods=['GET','POST'])
def delete():
    global selected
    id = request.args.get('id', '', type=str)
    type = request.args.get('type', '', type=str)

    if type == 'folder':
        id = id.split("-")[1]
        folder = db.session.query(Folder).get(id)
        db.session.delete(folder)
        db.session.commit()

        return json.dumps({'result': 'success'})

    elif type == "leaf":
        image = Image.query.filter_by(uri=id).first()
        db.session.delete(image)
        db.session.commit()

        os.remove(os.path.join(app.config["ROOT_PATH"], "static/uploads", id))

        return json.dumps({'result': 'success'})

    else:
        os.remove(os.path.join(app.config["ROOT_PATH"], "static/uploads", id))
        return json.dumps({'result': 'success'})

# @app.route('/ins_profile', methods=['GET', 'POST'])
# def ins_profile():
#     logger = logging.getLogger(__name__)
#
#     error = False
#     global selected
#     username = request.args.get('username')
#     password = request.args.get('password')
#     id = request.args.get('id')
#
#     max_id = 100
#     for i in range(5):
#         try:
#             instagram = Instagram(username, password, IGDataPath="/tmp/account_%d" % int(id))
#             instagram.login()
#
#             ins_profile = instagram.getProfileData()
#             profile_pic_url = ins_profile.profile_pic_url
#             ins_username = ins_profile.username
#             ins_fullname = ins_profile.full_name
#             biography = ins_profile.biography
#             website = ins_profile.external_url
#             follower_count = len(instagram.getSelfUserFollowers().followers)
#             following_cout = len(instagram.getSelfUsersFollowing().followings)
#
#             # posts = []
#             # for item in instagram.getSelfUserFeed(max_id).getItems():
#             #     post = Post()
#             #     post.image = [item.getImageVersions()[0].getUrl(), item.getImageVersions()[-1].getUrl()]
#             #     post.caption = item.getCaption().getText() if item.getCaption() else ""
#             #     post.posted_at = datetime.fromtimestamp(item.item["taken_at"])
#             #     posts.append(post)
#
#             break
#         except Exception:
#             logger.exception("Error retrieving posted posts", exc_info=True)
#
#     else:
#         profile_pic_url = ""
#         ins_username = ""
#         ins_fullname = ""
#         biography = ""
#         website = ""
#         follower_count = ""
#         following_cout = ""
#         posts = account.posts.filter(Post.posted_at != None)
#         error = True
#
#     return json.dumps({
#         "profile_pic_url": profile_pic_url,
#         "ins_username": ins_username,
#         "ins_fullname": ins_fullname,
#         "biography": biography,
#         'website': website,
#         "follower_count": follower_count,
#         "following_cout": following_cout,
#         # "posts": posts,
#         'error': error
#     })

