from flask import abort, flash, redirect, render_template, url_for, \
    request, current_app, session
from flask_login import current_user, login_required

from .forms import PayrollGroupForm
from app import db
from app.models import Payroll_Group
from app.library import bp

from app.flask_pager import Pager


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.has_role('admin'):
        abort(403)


# Payroll_Group Views
@bp.route('/payroll_group/', methods=['GET', 'POST'])
@login_required
def list_payroll_groups():
    """
    List all payroll groups
    """

    check_admin()

    search_text = request.args.get('search')

    title = 'Payroll Groups'

    if search_text is not None:
        payroll_groups = Payroll_Group.query\
            .filter(Payroll_Group.name.contains(search_text)).all()
        count = Payroll_Group.query\
            .filter(Payroll_Group.name.contains(search_text)).count()
    else:
        payroll_groups = Payroll_Group.query.all()
        count = Payroll_Group.query.count()

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1

    data = payroll_groups
    if data:
        pager = Pager(page, count)
        pages = pager.get_pages()
        skip = (page - 1) * current_app.config['PAGE_SIZE']
        limit = current_app.config['PAGE_SIZE']
        data_to_show = data[skip: skip + limit]
    else:
        pages = None
        data_to_show = None

    session['back_url'] = request.url

    return render_template('library/payroll_groups/payroll_groups.html',
                           payroll_groups=payroll_groups, title=title,
                           pages=pages, data_to_show=data_to_show)


@bp.route('/payroll_groups/add', methods=['GET', 'POST'])
@login_required
def add_payroll_group():
    """
    Add a payroll group to the database
    """
    check_admin()

    add_payroll_group = True

    form = PayrollGroupForm()
    if form.validate_on_submit():
        payroll_group = Payroll_Group(name=form.name.data)
        try:
            # add payroll group to the database
            db.session.add(payroll_group)
            db.session.commit()
            flash('You have successfully added a new payroll group.')
        except:
            # in case payroll group name already exists
            flash('Error: payroll group name already exists.')

        # redirect to payroll groups page
        if 'back_url' in session:
            return redirect(session['back_url'])
        return redirect(url_for('library.list_payroll_groups'))

    # load payroll group template
    return render_template('library/payroll_groups/payroll_group.html',
                           action="Add", add_payroll_group=add_payroll_group,
                           form=form, title="Add Payroll Group")


@bp.route('/payroll_groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_payroll_group(id):
    """
    Edit a payroll group
    """
    check_admin()

    add_payroll_group = False

    payroll_group = Payroll_Group.query.get_or_404(id)
    form = PayrollGroupForm(obj=payroll_group)
    if form.validate_on_submit():
        payroll_group.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the payroll group.')

        # redirect to the payroll groups page
        if 'back_url' in session:
            return redirect(session['back_url'])
        return redirect(url_for('library.list_payroll_groups'))

    form.name.data = payroll_group.name
    return render_template('library/payroll_groups/payroll_group.html',
                           action="Edit", add_payroll_group=add_payroll_group,
                           form=form, payroll_group=payroll_group,
                           title="Edit Payroll_Group")


@bp.route('/payroll_groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_payroll_group(id):
    """
    Delete a payroll group from the database
    """
    check_admin()

    payroll_group = Payroll_Group.query.get_or_404(id)
    payroll_group_name = payroll_group.name
    # delete confirmation is done at the template level
    db.session.delete(payroll_group)
    db.session.commit()
    flash("You have successfully deleted the payroll group '{}'."
          .format(payroll_group_name))

    # redirect to the payroll groups page
    if 'back_url' in session:
        return redirect(session['back_url'])
    return redirect(url_for('library.list_payroll_groups'))

    # return render_template(title="Delete Payroll Group")


@bp.route('/payroll_groups/members/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_payroll_group(id):
    """
    Manage payroll group members
    """
    check_admin()

    payroll_group = Payroll_Group.query.get_or_404(id)
    payroll_group_name = payroll_group.name

    title = 'Payroll Group Members'

    # redirect to the payroll groups page
    # if 'back_url' in session:
    #     return redirect(session['back_url'])
    # return redirect(url_for('library.list_payroll_groups'))

    return render_template('library/payroll_groups/payroll_group_members.html',
                           title=title)
