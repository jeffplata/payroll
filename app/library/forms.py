from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField,\
    SelectField
from wtforms.validators import DataRequired
from app import db
from app.models import Office, Payroll_Type


def Office_List():
    # pass
    return [(x.id, x.name) for x in db.session.query(Office).order_by(Office.name).all()]


def Payroll_Type_List():
    # pass
    return [(x.id, x.name) for x in db.session.query(Payroll_Type).all()]


class SectionForm(FlaskForm):
    """
    Form for admin to add or edit a section
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PayrollForm(FlaskForm):
    """
    Form to add or edit a payroll
    """
    office_id = SelectField('Office', coerce=int, choices=Office_List())
    date = DateField('Date', validators=[DataRequired()])
    payroll_type_id = SelectField('Type', coerce=int, choices=Payroll_Type_List())
    period = StringField('Period', validators=[DataRequired()])
    submit = SubmitField('Submit')
