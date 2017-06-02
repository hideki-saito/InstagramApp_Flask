from datetime import datetime, timedelta
import logging

import os
from PIL import Image, ImageFile


import dtech_instagram.pynstagram
from dtech_instagram.InstagramAPI import Instagram
from dtech_instagram.celery import cron
from dtech_instagram.db import db
from dtech_instagram.models import Account, Post, Ins_Profile, Ins_History, Ins_Posted

logger = logging.getLogger(__name__)


def inividual_analytic(account):
    instagram = Instagram(account.username, account.password, IGDataPath="/tmp/account_%s" % account.username)
    instagram.login()
    username_id = instagram.username_id

    account_profile = instagram.getProfileData()

    ins_profile = account.ins_profile
    if ins_profile is None:
        ins_profile = Ins_Profile()
    ins_profile.account_id = account.id
    ins_profile.pro_pic_url = account_profile.profile_pic_url
    ins_profile.username = account_profile.username
    ins_profile.full_name = account_profile.full_name
    ins_profile.bio = account_profile.biography
    ins_profile.website = account_profile.external_url

    db.session.add(ins_profile)
    db.session.commit()

    lifetime_posts_count = 0
    lifetime_likes_count = 0
    lifetime_comments_count = 0
    maxid = None
    while True:
        account_feed = instagram.getSelfUserFeed(maxid)
        lifetime_posts_count = lifetime_posts_count + len(account_feed.items)
        for item in account_feed.items:
            lifetime_likes_count = lifetime_likes_count + item.like_count
            lifetime_comments_count = lifetime_comments_count + item.comment_count

            media_id = item.id
            ins_posted = db.session.query(Ins_Posted).get(media_id)
            if ins_posted is None:
                ins_posted = Ins_Posted()

            ins_posted.media_id = media_id
            ins_posted.account_id = account.id
            ins_posted.code = item.code
            ins_posted.pic_url = item.getImageVersions()[0].getUrl()
            ins_posted.thum_url = item.getImageVersions()[-1].getUrl()
            ins_posted.caption = item.getCaption().getText() if item.getCaption() else ""
            ins_posted.likes_count = item.like_count
            ins_posted.comments_count = item.comment_count
            ins_posted.taken_at = datetime.fromtimestamp(item.taken_at).strftime('%Y-%m-%d %H:%M:%S')

            db.session.add(ins_posted)
            db.session.commit()

        maxid = account_feed.next_max_id
        if maxid is None:
            break

    # today = datetime.utcnow().date()
    # ins_history = db.session.query(Ins_History).get(Ins_History.history_at==today)
    # if ins_history is None:
    ins_history = Ins_History()
    ins_history.account_id = account.id
    ins_history.history_at = datetime.utcnow()

    max_id = ""
    account_followsers_count = 0
    while True:
        account_follow_response = instagram.getUserFollowers(username_id, max_id)
        account_followsers_count = account_followsers_count + len(account_follow_response.followers)

        max_id = account_follow_response.next_max_id
        if max_id is None:
            break

    ins_history.followers_count = account_followsers_count

    max_id = ""
    account_followings_count = 0
    while True:
        account_following_response = instagram.getUserFollowings(username_id, max_id)
        account_followings_count = account_followings_count + len(account_following_response.followings)

        max_id = account_following_response.next_max_id
        if max_id is None:
            break

    ins_history.followings_count = account_followings_count

    ins_history.posts_count = lifetime_posts_count
    ins_history.likes_count = lifetime_likes_count
    ins_history.comments_count = lifetime_comments_count

    db.session.add(ins_history)
    db.session.commit()


@cron.job(timedelta(seconds=120))
def ins_analytics():
    accounts = Account.query.all()
    for account in accounts:
        inividual_analytic(account)

