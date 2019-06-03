from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Staff

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    fullname = StringField('Fullname', validators=[DataRequired()], render_kw={"placeholder": "Full name"})
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Retype password"})
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Staff.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
