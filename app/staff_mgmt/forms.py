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
