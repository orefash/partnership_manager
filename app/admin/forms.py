from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo



class PartnerDataEntry(FlaskForm):
    """
    Form for users to login
    """
    title = StringField('Title', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Title"})
    surname = StringField('Surname', validators=[DataRequired()], render_kw={"placeholder": "Enter Surname"})
    fname = StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Enter First Name"})
    phone = StringField('Phone', render_kw={"placeholder": "Enter Phone number"})
    email = StringField('Email', render_kw={"placeholder": "Enter Email"})
    kchat = StringField('Kingschat', render_kw={"placeholder": "Enter Kingschat no."})
    amount = StringField('Amount', validators=[DataRequired()], render_kw={"placeholder": "Enter Amount"})
    submit = SubmitField('Submit')

