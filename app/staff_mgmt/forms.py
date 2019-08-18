from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Staff


class StaffForm(FlaskForm):

    fname = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "Enter First Name"})
    surname = StringField('Surname', validators=[DataRequired()], render_kw={"placeholder": "Enter Surname"})
    phone = StringField('Phone', validators=[DataRequired()] , render_kw={"placeholder": "Enter Phone number"})
    email = EmailField('Email', validators=[DataRequired(), Email()] , render_kw={"placeholder": "Enter Email"})
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    """
    Form for users to create new account
    """

    old_password = PasswordField('Current Password', render_kw={"placeholder": "Current password"})
    password = PasswordField('New Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ], render_kw={"placeholder": "New password"})
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Retype new password"})
    submit = SubmitField('Submit')
