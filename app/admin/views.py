from flask import flash, redirect, render_template, url_for, send_file, send_from_directory
from flask_login import current_user, login_required
from flask import request
from flask import jsonify
from sqlalchemy import or_
from sqlalchemy import text

import os, app

# from app import app

from . import admin
from forms import PartnerDataEntry

from datetime import datetime
from .. import db, APP_ROOT

from ..models import Staff, Member, Group, Church, Pcf, Cell, PartnerGiving, PartnershipArm

from data_helper import get_p_table_header, get_partnerships, get_partnership_data, get_partnership_data_by_date


APP_ROOT = APP_ROOT
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
D_FOLD = 'static/reports'
D_FOLDER = os.path.join(APP_ROOT, D_FOLD)

@admin.route('/get-church/<group>')
def get_church(group):
    churches = Church.query.with_entities(Church.id, Church.church).filter_by(group_id=group).all()

    # print(churches)

    return jsonify(churches)

@admin.route('/get-arms')
def get_arms():
    p_arms = get_partnerships()

    return jsonify(p_arms)

@admin.route('/get-cell/<pcf>')
def get_cell(pcf):
    cells = Cell.query.with_entities(Cell.id, Cell.cell).filter_by(pcf_id=pcf).all()

    return jsonify(cells)

def check_member(phone, email):
    member = Member.query.filter(or_(Member.phone == phone, Member.email == email)).first()
    if member is None:
        return -1
    else:
        return member.id



@admin.route('/data-entry/partnership', methods=['GET', 'POST'])
@login_required
def enter_partnership():
    """
    Render the homepage template on the / route
    """
    groups = Group.query.with_entities(Group.id, Group.group).all()

    # groups = Group.query.with_entities(Group.id, Group.group).all()
    pcfs = Pcf.query.with_entities(Pcf.id, Pcf.pcf).all()

    p_arms = PartnershipArm.query.with_entities(PartnershipArm.id, PartnershipArm.partnership_arm).all()

    form = PartnerDataEntry(groups)
    if request.method == 'POST':
        print("After post check")

        title = request.form['title']
        surname = request.form['surname']
        fname = request.form['fname']
        phone = request.form['phone']
        email = request.form['email']
        grp = request.form['grp']
        group = request.form['group']
        church = request.form['church']
        pcf = request.form['pcf']
        cell = request.form['cell']
        arm = request.form['arm']
        kchat = request.form['kchat']
        amount = request.form['amount']
        staff = current_user
        entry_date = datetime.today().strftime('%Y-%m-%d')

        additional_field_count = request.form['field_count']

        is_pledge = True if grp == '1' else False

        print("Additional: ",additional_field_count)

        # print("Title "+title+" Sn "+surname+" fname "+fname+" phone "+phone+" GRP: "+grp+" GRouP: "+group+" Church: "+church+" PCF: "+pcf+" Cell: "+cell)
        # print('Arm: '+arm+" Staff: "+staff.f_name)

        member = Member( group_id=group, church_id=church, pcf_id=pcf, cell_id=cell, title=title, l_name=surname, f_name=fname, phone=phone, email=email, kingschat_no=kchat, entry_date=entry_date)
        # print(member)
        status = check_member(phone, email)

        m_id = status
        if status == -1:
            db.session.add(member)
            db.session.flush()

            m_id = member.id

        partner_giving = PartnerGiving(member_id=m_id, arm_id=arm, staff_id=staff.id, amount=amount, is_pledge=is_pledge, entry_date=entry_date)
        db.session.add(partner_giving)

        print("In others: ")
        for i in range(1, int(additional_field_count)+1):
            arm = request.form['arm'+str(i)]
            amount = request.form['amount'+str(i)]
            # print("arm: "+arm+" amount: "+amount)

            partner_giving = PartnerGiving(member_id=m_id, arm_id=arm, staff_id=staff.id, amount=amount, is_pledge=is_pledge, entry_date=entry_date)
            db.session.add(partner_giving)


        db.session.commit()

        return redirect(url_for('admin.enter_partnership'))

    return render_template('data_entry_partnership.html', form=form, title="Partnership Entry", active=1, groups=groups, pcfs=pcfs, parms=p_arms)

@admin.route('/data-entry/tithe')
@login_required
def enter_tithe():
    """
    Render the homepage template on the / route
    """
    return render_template('data_entry_tithe.html', title="Tithe Entry", active=2)

@admin.route('/get-partner-data/<start>/<end>')
def get_p_by_date(start, end):

    # start = '2019/02/01'
    # end = '2019/04/01'

    data = get_partnership_data_by_date(start, end)
    # print("response: ",data)

    return jsonify(data)


@admin.route('/get-data-report')
def get_data_report():
    # print("root: ",root_dir)
    # return root_dir

    report_dir = os.path.join(APP_ROOT, 'static', 'reports')
    report_dir_file = os.path.join(APP_ROOT, 'static', 'reports', 'CARD.png')
    # report_dir = url_for('static', filename='reports/CARD.png')
    # report_dir = D_FOLDER
    print("static: ",report_dir_file)
    # return "hello"

    # if path is None:

    try:
        return send_file(report_dir_file, as_attachment=True)
        # return send_from_directory(report_dir, filename='CARD.png', as_attachment=True)
    except Exception as e:
        print("exc: ",str(e))
        return str(e)


@admin.route('/data-view/partnership')
@login_required
def view_partnership():
    """
    Render the homepage template on the / route
    """
    header =  get_p_table_header()

    partner_data = get_partnership_data()

    return render_template('view_partnerships.html', title="View Partnership", active=3, header=header, partner_data=partner_data)

@admin.route('/data-view/tithe')
@login_required
def view_tithe():
    """
    Render the homepage template on the / route
    """
    return render_template('view_tithes.html', title="View Tithe", active=4)

@admin.route('/data-view/incorporations')
@login_required
def view_incorporations():
    """
    Render the homepage template on the / route
    """
    return render_template('view_incorporation.html', title="Partner Incorporations", active=5)
