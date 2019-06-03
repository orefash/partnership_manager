from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
