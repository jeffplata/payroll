from flask import abort, flash, redirect, render_template, url_for, \
    request, current_app
from flask_login import current_user, login_required

from .forms import SectionForm
from app import db
from app.models import Section
from app.library import bp

from app.flask_pager import Pager


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.has_role('admin'):
        abort(403)


# Section Views
@bp.route('/sections/', methods=['GET', 'POST'])
# @bp.route('/sections/<search>', methods=['GET', 'POST'])
# @bp.route('/sections/<page>', methods=['GET', 'POST'])
# @bp.route('/sections/<search>/<page>', methods=['GET', 'POST'])
@login_required
def list_sections():
    """
    List all sections
    """

    check_admin()

    search_text = request.args.get('search')

    title = 'Sections'

    if search_text is not None:
        sections = Section.query.filter(Section.name.contains(search_text)).all()
        count = Section.query.filter(Section.name.contains(search_text)).count()
    else:
        sections = Section.query.all()
        count = Section.query.count()

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1

    data = sections
    if data:
        pager = Pager(page, count)
        pages = pager.get_pages()
        skip = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[skip: skip + limit]
    else:
        pages = None
        data_to_show = None

    return render_template('library/sections/sections.html',
                           sections=sections, title=title,
                           pages=pages, data_to_show=data_to_show)


@bp.route('/sections/add', methods=['GET', 'POST'])
@login_required
def add_section():
    """
    Add a section to the database
    """
    check_admin()

    add_section = True

    form = SectionForm()
    if form.validate_on_submit():
        section = Section(name=form.name.data)
        try:
            # add section to the database
            db.session.add(section)
            db.session.commit()
            flash('You have successfully added a new section.')
        except:
            # in case section name already exists
            flash('Error: section name already exists.')

        # redirect to sections page
        return redirect(url_for('library.list_sections'))

    # load section template
    return render_template('library/sections/section.html', action="Add",
                           add_section=add_section, form=form,
                           title="Add Section")


@bp.route('/sections/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_section(id):
    """
    Edit a section
    """
    check_admin()

    add_section = False

    section = Section.query.get_or_404(id)
    form = SectionForm(obj=section)
    if form.validate_on_submit():
        section.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the section.')

        # redirect to the sections page
        # return redirect(url_for('library.list_sections'))
        return redirect(request.referrer)
        # TODO: find the referrer page

    form.name.data = section.name
    return render_template('library/sections/section.html', action="Edit",
                           add_section=add_section, form=form,
                           section=section, title="Edit Section")


@bp.route('/sections/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_section(id):
    """
    Delete a section from the database
    """
    check_admin()

    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash('You have successfully deleted the section.')

    # redirect to the sections page
    return redirect(url_for('library.list_sections'))

    return render_template(title="Delete Section")
