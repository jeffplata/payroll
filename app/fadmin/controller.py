from app.fadmin import bp
from flask import url_for, flash, redirect
from flask_user import current_user, roles_required

from flask_admin.menu import MenuLink
from flask_admin import Admin, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView

from app import db
from app.user_models import User, Role
from flask import current_app, render_template, request

from werkzeug import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from sqlalchemy.orm.attributes import InstrumentedAttribute

# app specifics
from app.models import Section, Office, Salary_reference, Salary, \
    Position, Plantilla, Plantilla_type


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
    column_filter_labels = []
    search_placeholder_text = []

    # Customize the filter labels if desired
    #   (define column_filter_labels)
    def scaffold_filters(self, name):
        filters = super().scaffold_filters(name)
        if name in self.column_filter_labels:
            for f in filters:
                f.name = self.column_filter_labels[name]
        return filters

    # Customize the search placeholders if desired
    #   (define search_placeholder_text)
    def search_placeholder(self):
        placeholders = super().search_placeholder()
        if self.search_placeholder_text:
            placeholders = self.search_placeholder_text
            placeholders = 'Search: '+u', '.join(placeholders)
        return placeholders


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


# App specific views
class MyAppLibraryView(MyModelView):
    column_searchable_list = ['name', ]
    form_excluded_columns = ['date_created', 'date_modified', ]
    column_display_pk = True


class MyAppLibraryViewNoName(MyModelView):
    form_excluded_columns = ['date_created', 'date_modified', ]
    column_display_pk = True


class MyAppLibraryViewSalary(MyAppLibraryViewNoName):
    column_list = ('sg', 'step', 'amount', 'salary_reference')
    form_columns = column_list
    column_filters = ('sg', 'step')


class MyAppLibraryViewPlantilla(MyAppLibraryViewNoName):
    column_list = ('id', 'itemno', 'sg', 'position', 'office', 'section',
                   'plantilla_type')
    form_columns = column_list
    column_searchable_list = (Plantilla.itemno, Position.name, Office.name,
                              Section.name)
    search_placeholder_text = ['Item No.', 'Position', 'Office', 'Section']
    column_filters = (Position.name, Office.name, Section.name,
                      Plantilla_type.name, 'sg')
    column_filter_labels = {Position.name: 'Position', Office.name: 'Office',
                            Section.name: 'Section',
                            Plantilla_type.name: 'Type', 'sg': 'Salary Grade'}


admin.add_view(MyAppLibraryView(Section, db.session))
admin.add_view(MyAppLibraryView(Office, db.session))
admin.add_view(MyAppLibraryViewNoName(Salary_reference, db.session))
admin.add_view(MyAppLibraryViewSalary(Salary, db.session))
admin.add_view(MyAppLibraryView(Position, db.session))
admin.add_view(MyAppLibraryView(Plantilla_type, db.session))
admin.add_view(MyAppLibraryViewPlantilla(Plantilla, db.session))

# End: App specific views


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
    filename = FileField('Select Excel Source File')
    submit = SubmitField('Import Selected File')


@bp.route('/library-import/<library>', methods=['GET', 'POST'])
@roles_required('admin')
def library_import(library):
    if library == 'Section':
        tables = [Section]
    elif library == 'Office':
        tables = [Office]
    elif library == 'Salary':
        tables = [Salary]
    elif library == 'Position':
        tables = [Position]
    elif library == 'Plantilla':
        tables = [Plantilla]
    title = 'Import to '+library
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.filename.data.filename)
        request.save_book_to_database(
            field_name='filename', session=db.session,
            tables=tables,)
        flash("You have successfully imported '{}' to {}".format(filename, library))
        return redirect(url_for('admin.index'))
    else:
        filename = None
    return MyView().render("fadmin/import_library.html", form=form, title=title)
