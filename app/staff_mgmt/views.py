from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from flask import request
from forms import StaffForm

from . import staff_mgmt
from .. import db
from ..models import Staff, Staff_Role

from datetime import datetime

from data_helper import get_staff_details

@staff_mgmt.route('/staff', methods=['GET', 'POST'])
def manage_staff():

    staff = get_staff_details()

    return render_template('manage_staff.html', staff=staff, title="Manage Staff")

@staff_mgmt.route('/delete-staff/<s_id>')
def remove_staff(s_id):

    Staff.query.filter_by(id=s_id).delete()
    db.session.commit()

    return redirect(url_for('staff_mgmt.manage_staff'))

@staff_mgmt.route('/add-staff', methods=['GET', 'POST'])
def add_staff():
    form = StaffForm()
    roles = Staff_Role.query.with_entities(Staff_Role.id, Staff_Role.role).all()
    print("Role:", roles)

    if request.method == 'POST':
        surname = request.form['surname']
        fname = request.form['fname']
        phone = request.form['phone']
        email = request.form['email']
        role = request.form['role']

        # print("Details: "+surname+" "+fname+" "+phone+" "+email+" "+role)
        staff = Staff(
        role_id=role,
        email=email,
        f_name=fname,
        l_name=surname,
        phone=phone,
        entry_date = datetime.today().strftime('%Y-%m-%d'),
        password_hash='password')
        db.session.add(staff)
        db.session.commit()
        # flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('staff_mgmt.manage_staff'))

    # staff = get_staff_details()

    return render_template('add_staff.html', form = form, title="Add Staff")
