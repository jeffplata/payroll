from app.fadmin import bp
from flask import url_for
from flask_user import current_user

from flask_admin.menu import MenuLink
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from app import db
from app.user_models import User, Role
from flask import current_app, render_template, request

from werkzeug import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from app.models import Section


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (not current_user.is_anonymous) and current_user.has_role('admin')


app_name = current_app.config['USER_APP_NAME']

admin = Admin(name=app_name+' Admin', template_mode='bootstrap3',
              index_view=MyAdminIndexView(template='fadmin/index.html'))


class MyModelView(ModelView):
    def is_accessible(self):
        return (not current_user.is_anonymous) and current_user.has_role('admin')
    page_size = 25
    can_view_details = True
    edit_modal = True
    column_hide_backrefs = False
    can_export = True


class MyUserModelView(MyModelView):
    column_exclude_list = ['password_hash', ]
    column_searchable_list = ['username', 'email']
    column_list = ('username', 'email', 'date_created', 'date_modified', 'roles')
    form_excluded_columns = ['date_created', 'date_modified', 'password']


class MyRoleModelView(MyModelView):
    column_list = ('name', 'date_created', 'date_modified')
    form_excluded_columns = ['date_created', 'date_modified', ]


admin.add_view(MyUserModelView(User, db.session))
admin.add_view(MyRoleModelView(Role, db.session))


@bp.before_app_first_request
def assign_links_to_admin():
    admin.add_link(MenuLink(name='Public Website', category='', url=url_for('main.index')))
    admin.add_link(MenuLink(name='Logout', category='', url=url_for('user.logout')))


class MyView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = False
        super(MyView, self).__init__(*args, **kwargs)
        self.admin = admin


class UploadForm(FlaskForm):
    filename = FileField('Select and Excel Source File')
    submit = SubmitField('Import Selected File')


@bp.route('/sections-import', methods=['GET', 'POST'])
def sections_import():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.filename.data.filename)
        request.save_book_to_database(
            field_name='filename', session=db.session,
            tables=[Section],)
    else:
        filename = None
    return MyView().render("fadmin/import_sections.html", form=form)
