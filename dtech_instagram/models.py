from flask_security import UserMixin, RoleMixin

from dtech_instagram.db import db


roles_users = db.Table("roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), unique=True)
    description = db.Column(db.Text())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), nullable=True)
    max_accounts = db.Column(db.Integer(), default=1)
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __str__(self):
        return "<User id=%s email=%s>" % (self.id, self.email)


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    username = db.Column(db.Text())
    password = db.Column(db.Text())

    user = db.relationship("User", backref=db.backref("accounts", order_by="Account.username",
                                                                  cascade="all,delete-orphan"))


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.Integer(), db.ForeignKey("account.id", ondelete="CASCADE"))
    image = db.Column(db.Text())
    caption = db.Column(db.Text())
    post_at = db.Column(db.DateTime())
    post_at_timezone_offset = db.Column(db.Integer())
    posted_at = db.Column(db.DateTime(), nullable=True)

    account = db.relationship("Account", backref=db.backref("posts", order_by="desc(Post.post_at)",
                                                                     cascade="all,delete-orphan",
                                                                     lazy="dynamic"))
class Folder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    name = db.Column(db.Text())

    user = db.relationship("User", backref=db.backref("folders", order_by="Folder.id",
                                                      cascade="all, delete-orphan",
                                                      lazy="dynamic"))

class Image(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    folder_id = db.Column(db.Integer(), db.ForeignKey("folder.id", ondelete="CASCADE"))
    name = db.Column(db.Text())
    uri = db.Column(db.Text())

    folder = db.relationship("Folder", backref=db.backref("images",
                                                                  cascade="all,delete-orphan", lazy="dynamic"))
