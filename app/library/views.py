from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

# from . import admin
from .forms import SectionForm
from app import db
from app.models import Section
from app.library import bp


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.has_role('admin'):
        abort(403)


# Section Views


@bp.route('/sections', methods=['GET', 'POST'])
@login_required
def list_sections():
    """
    List all sections
    """
    
    check_admin()

    sections = Section.query.all()

    return render_template('library/sections/sections.html',
                           sections=sections, title="Sections")


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
        return redirect(url_for('library.list_sections'))

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
