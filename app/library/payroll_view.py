from flask import (abort, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required

from app import db
from app.flask_pager import Pager
from app.library import bp
from app.models import Payroll, Payroll_Type, Office, Payroll_Employees,\
    Employee_Detail, Plantilla, Employee, Payroll_Earnings,\
    Payroll_Type_Earnings

from .forms import PayrollForm
from datetime import date
from sqlalchemy import or_


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
        payrolls = Payroll.query.join(Payroll_Type).join(Office).filter(or_(
                                        Payroll_Type.name.contains(search_text),
                                        Office.name.contains(search_text)
                                 )).order_by(Payroll.id.desc()).all()
        count = Payroll.query.join(Payroll_Type).join(Office).filter(or_(
                                        Payroll_Type.name.contains(search_text),
                                        Office.name.contains(search_text)
                                 )).count()
    else:
        payrolls = Payroll.query.order_by(Payroll.id.desc()).all()
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
                          payroll_type_id=form.payroll_type_id.data,
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
        payroll.payroll_type_id = form.payroll_type_id.data
        payroll.period = form.period.data
        db.session.commit()
        flash('You have successfully edited the payroll.')

        # redirect to the payrolls page
        if 'back_url' in session:
            return redirect(session['back_url'])
        return redirect(url_for('library.list_payrolls'))

    form.office_id.data = payroll.office_id
    form.date.data = payroll.date
    form.payroll_type_id.data = payroll.payroll_type_id
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


@bp.route('/payrolls/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def payroll_detail(id):
    """
    Show payroll details
    """

    # check_admin()

    title = 'Payroll Detail'
    payroll = Payroll.query.get_or_404(id)
    """
    payroll_lines = Payroll_Employees.query.\
        filter(Payroll_Employees.payroll_id == id).all()

    if not payroll_lines:
        # there are no data yet
        employees = Employee_Detail.query.join(Plantilla).join(Employee).\
            filter(Plantilla.office_id == payroll.office_id).\
            order_by(Employee.last_name, Employee.first_name).all()

        for e in employees:
            pe = Payroll_Employees(payroll_id=id, employee_id=e.employee_id)
            db.session.add(pe)
        db.session.commit()
        payroll_lines = Payroll_Employees.query.\
            filter(Payroll_Employees.payroll_id == id).all()
    """
    payroll_lines = Payroll_Earnings.query.\
        filter(Payroll_Earnings.payroll_id == id).all()

    earnings = Payroll_Type_Earnings.query.\
        filter_by(payroll_type_id=payroll.payroll_type_id)

    if not payroll_lines:
        # there are no data yet
        employees = Employee_Detail.query.join(Plantilla).join(Employee).\
            filter(Plantilla.office_id == payroll.office_id).\
            order_by(Employee.last_name, Employee.first_name).all()

        for e in employees:
            for ea in earnings:
                pe = Payroll_Earnings(payroll_id=id, employee_id=e.employee_id,
                                      earnings_id=ea.earnings_id, amount=100)
                db.session.add(pe)
        db.session.commit()
        payroll_lines = Payroll_Earnings.query.\
            filter(Payroll_Earnings.payroll_id == id).all()

    # cross-tabulate payroll lines
    # for pl in payroll_lines:
    # x = [i for i, v in enumerate(payroll_lines) if v.employee_id == 73].pop()

    seen = set()
    new_tuple = []
    for item in payroll_lines:
        if item.employee_id not in seen:
            new_tuple.append([item.employee_id, item.employee.employee_no, item.employee.full_name])
            seen.add(item.employee_id)

    new_list = list(new_tuple)
    for item in new_list:
        print(item + ['ssss'])


    return render_template('library/payrolls/payroll_detail.html',
                           payroll=payroll, payroll_lines=payroll_lines,
                           title=title)
