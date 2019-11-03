from flask import (abort, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required

from app import db
from app.flask_pager import Pager
from app.library import bp
from app.models import Payroll

from .forms import PayrollForm
from datetime import date


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.has_role('admin'):
        abort(403)


# Payroll Views
@bp.route('/payrolls/', methods=['GET', 'POST'])
@login_required
def list_payrolls():
    """
    List all payrolls
    """

    # check_admin()

    search_text = request.args.get('search')

    title = 'Payrolls'

    if search_text is not None:
        payrolls = Payroll.query.filter(Payroll.payroll_type.name.contains(search_text)).all()
        count = Payroll.query.filter(Payroll.payroll_type.name.contains(search_text)).count()
    else:
        payrolls = Payroll.query.all()
        count = Payroll.query.count()

    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1

    data = payrolls
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

    return render_template('library/payrolls/payrolls.html',
                           payrolls=payrolls, title=title,
                           pages=pages, data_to_show=data_to_show)


@bp.route('/payrolls/add', methods=['GET', 'POST'])
@login_required
def add_payroll():
    """
    Add a payroll to the database
    """
    # check_admin()

    add_payroll = True

    form = PayrollForm()
    if form.validate_on_submit():
        payroll = Payroll(office_id=form.office_id.data,
                          date=form.date.data,
                          payroll_type_id=form.payroll_type.data,
                          period=form.period.data)
        try:
            # add payroll to the database
            db.session.add(payroll)
            db.session.commit()
            flash('You have successfully added a new payroll.')
        except:
            # in case payroll name already exists
            flash('Error: payroll cannot be saved.')

        # redirect to payrolls page
        if 'back_url' in session:
            return redirect(session['back_url'])
        return redirect(url_for('library.list_payrolls'))

    form.date.data = date.today()
    # load payroll template
    return render_template('library/payrolls/payroll.html', action="Add",
                           add_payroll=add_payroll, form=form,
                           title="Add payroll")


@bp.route('/payrolls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_payroll(id):
    """
    Edit a payroll
    """
    # check_admin()

    add_payroll = False

    payroll = Payroll.query.get_or_404(id)
    form = PayrollForm(obj=payroll)
    if form.validate_on_submit():
        payroll.office_id = form.office_id.data
        payroll.date = form.date.data
        payroll.payroll_type = form.payroll_type.data
        payroll.period = form.period.data
        db.session.commit()
        flash('You have successfully edited the payroll.')

        # redirect to the payrolls page
        if 'back_url' in session:
            return redirect(session['back_url'])
        return redirect(url_for('library.list_payrolls'))

    form.office_id.data = payroll.office_id
    form.date.data = payroll.date
    form.payroll_type.data = payroll.payroll_type
    form.period.data = payroll.period

    return render_template('library/payrolls/payroll.html', action="Edit",
                           add_payroll=add_payroll, form=form,
                           payroll=payroll, title="Edit payroll")


@bp.route('/payrolls/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_payroll(id):
    """
    Delete a payroll from the database
    """
    check_admin()

    payroll = Payroll.query.get_or_404(id)
    # if window.confirm('Delete '+payroll.name):
    db.session.delete(payroll)
    db.session.commit()
    flash('You have successfully deleted the payroll.')

    # redirect to the payrolls page
    # return redirect(url_for('library.list_payrolls'))
    if 'back_url' in session:
        return redirect(session['back_url'])
    return redirect(url_for('library.list_payrolls'))

    # return render_template(title="Delete payroll")
