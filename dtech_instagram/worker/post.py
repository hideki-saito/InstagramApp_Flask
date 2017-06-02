from datetime import datetime, timedelta
import logging
import os
from PIL import Image, ImageFile

import dtech_instagram.pynstagram

from dtech_instagram.app import app
from dtech_instagram.celery import cron
from dtech_instagram.db import db
from dtech_instagram.models import Post

logger = logging.getLogger(__name__)

@cron.job(timedelta(seconds=60))
def make_postings():
    for post in db.session.query(Post).filter(Post.posted_at == None):
        if post.post_at + timedelta(seconds=post.post_at_timezone_offset) <= datetime.utcnow():
            try:
                photo = os.path.join(app.config["ROOT_PATH"], "static/uploads", post.image)
                im = Image.open(photo)
                ImageFile.MAXBLOCK = 2 ** 20
                photo += ".jpg"
                logger.debug(im.size)
                if im.size[0] > 1080 or im.size[1] > 1350:
                    im.resize((1080, 1350), Image.ANTIALIAS).save(photo, "JPEG", quality=100, optimize=True, progressive=True)
                elif im.size[0] != im.size[1]:
                    logger.debug('changin the aspect ratios')
                    new_size = min(im.size[0], im.size[1])
                    im.resize((new_size, new_size), Image.ANTIALIAS).save(photo, "JPEG", quality=100, optimize=True,
                                                              progressive=True)
                else:
                    im.save(photo, "JPEG", quality=100, optimize=True, progressive=True)

                with dtech_instagram.pynstagram.client(post.account.username, post.account.password) as client:
                    client.upload(photo, post.caption)

                post.posted_at = datetime.utcnow()
                db.session.commit()
            except Exception:
                logger.error("Error posting photo", exc_info=True)
