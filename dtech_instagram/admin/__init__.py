# -*- coding=utf-8 -*-
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib import sqla
from flask_security import current_user, utils
import logging
from wtforms.fields import PasswordField

from dtech_instagram.app import app
from dtech_instagram.db import db
from dtech_instagram.models import User

logger = logging.getLogger(__name__)

__all__ = []


class AuthorizedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        return app.login_manager.unauthorized()


class UserAdmin(sqla.ModelView):
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.new_password = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.new_password):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.new_password)

admin = Admin(app, index_view=AuthorizedAdminIndexView(),
              base_template="admin_base.html", template_mode="bootstrap3")

# Add Flask-Admin views for Users and Roles
admin.add_view(UserAdmin(User, db.session))
