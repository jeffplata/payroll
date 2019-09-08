from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SectionForm(FlaskForm):
    """
    Form for admin to add or edit a section
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
