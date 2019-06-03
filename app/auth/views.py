from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from flask import request

from . import auth
from forms import LoginForm , RegistrationForm
from .. import db
from ..models import Staff

from datetime import datetime

# @auth.route('/login')
# def user_login():
#     """
#     Render the homepage template on the / route
#     """
#     return render_template('login.html', title="Login")

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    print "In login"
    form = LoginForm()
    if request.method == 'POST':
        print("After post check")
        email = request.form['email']
        password = request.form['password']
        print("Email ",email)
        staff = Staff.query.filter_by(email=email).first()
        print("Staff", staff)
        if staff is not None and staff.verify_password(password):
            # log employee in
            login_user(staff)

            # redirect to the dashboard page after login
            return redirect(url_for('home.show_dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def user_logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    # flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.user_login'))

@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    """
    Render the homepage template on the / route
    """
    print "In register"
    form = RegistrationForm()
    if request.method == 'POST':
        print("After post check")
        email = request.form['email']
        password = request.form['password']
        print("Email ",email)

        fullname = form.fullname.data
        names = fullname.split()
        print("Name: "+fullname)
        n_len = len(names)
        fn = ''
        ln = ''
        if n_len>=2:
            fn = names[0]
            ln = " ".join(names[1:])
        elif n_len<2 and n_len!=0:
            fn = names[0]


        staff = Staff(
        role_id='R01',
        email=form.email.data,
        f_name=fn,
        l_name=ln,
        phone='0801234567',
        entry_date = datetime.today().strftime('%Y-%m-%d'),
        password=form.password.data)

        # add employee to the database
        db.session.add(staff)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.user_login'))
    return render_template('register.html', form=form, title="Register")
