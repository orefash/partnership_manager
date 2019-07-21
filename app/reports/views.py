from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask import request
from flask import jsonify, current_app as app
from sqlalchemy import or_
from sqlalchemy import text
from flask_mail import Mail,  Message

from . import reports

from datetime import datetime
from .. import db, chart_colors

from ..models import Staff, Member, Group, Church, Pcf, Cell, PartnerGiving, PartnershipArm

from data_helper import get_members_data, get_cell_performance, get_pcfs_data, get_arm_count_by_pcf_member, get_pcf_data, get_pcf_member_partnership, get_monthly_partnership_pcf , get_member_partnership, get_arms, get_member_data, get_monthly_partnership, get_arm_count_by_member

import babel.numbers
import decimal
from babel.numbers import format_decimal
from babel.numbers import format_currency


@reports.route('/reports/members')
@login_required
def view_member_reports():

    # print("test a: ", a)

    members = get_members_data()
    # print(memberss)
    return render_template('view_members_reports.html', title="Partners List", members=members, active=6)

@reports.route('/reports/pcfs')
@login_required
def view_pcf_reports():
    pcfs = get_pcfs_data()
    # print(pcfs)
    return render_template('view_pcf_reports.html', pcfs = pcfs, title="PCF List", active=7)

@reports.route('/reports/member/<m_id>')
@login_required
def view_member_report(m_id):
    """
    Render the homepage template on the / route
    """
    partner_data = get_member_partnership(m_id)
    member_data = get_member_data(m_id)
    monthly_partnership = get_monthly_partnership(m_id)
    # print (format_currency(1099.98, 'NGN', locale='en_US'))

    end = partner_data[len(partner_data)-1]
    pledge_val = end[1]
    giving_val = end[2]
    # print("Giving: ",giving_val)
    # print("Pledge: ",pledge_val)

    total_giving = format_currency(giving_val, 'NGN', locale='en_US')
    total_pledge = format_currency(pledge_val, 'NGN', locale='en_US')

    arms = get_arm_count_by_member(m_id)
    arms_count = len(arms)

    # print("G: {giving} , P: {pledge}".format(giving=total_giving, pledge=total_pledge))

    print("arms: ",arms)
    # print('reasb: ',b)
    return render_template('partner_report.html', title="Partner Report", total_giving=total_giving, total_pledge=total_pledge, arms_count=arms_count, partner_data=partner_data, member_data=member_data, monthly_partnership=monthly_partnership)

@reports.route('/member-mail')
def member_mail():
    m_id = 4
    partner_data = get_member_partnership(m_id)
    member_data = get_member_data(m_id)

    return render_template('mails/partner-report.html', partner_data=partner_data, member_data=member_data)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = ''
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@reports.route('/send-member-report')
@login_required
def send_member_report():

    m_id = 4
    partner_data = get_member_partnership(m_id)
    member_data = get_member_data(m_id)

    print("Sending mail")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'kingfash5@gmail.com'
    MAIL_PASSWORD = 'AllHail1Me'

    app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'kingfash5@gmail.com',
    MAIL_PASSWORD = 'AllHail1Me'
	)

    mail = Mail(app)
    msg = Message("Send Mail Tutorial!",
      sender="kingfash5@gmail.com",
      recipients=["orefash@gmail.com"])
    msg.html = render_template('mails/partner-report.html', partner_data=partner_data, member_data=member_data)
    msg.body = ""

    try:
        mail.send(msg)
        return 'Mail sent!'
    except Exception, e:
		return(str(e))


@reports.route('/reports/pcf/<m_id>')
@login_required
def view_pcf_report(m_id):

    partner_data = get_pcf_member_partnership(m_id)
    member_data = get_pcf_data(m_id)
    monthly_partnership = get_monthly_partnership_pcf(m_id)
    # print (format_currency(1099.98, 'NGN', locale='en_US'))
    cell_performance = get_cell_performance(m_id)


    end = partner_data[len(partner_data)-1]
    pledge_val = end[1]
    giving_val = end[2]
    print("Giving: ",giving_val)
    print("Pledge: ",pledge_val)

    total_giving = format_currency(giving_val, 'NGN', locale='en_US')
    total_pledge = format_currency(pledge_val, 'NGN', locale='en_US')

    arms = get_arm_count_by_pcf_member(m_id)
    # arms_count = 4
    arms_count = len(arms)

    # print("G: {giving} , P: {pledge}".format(giving=total_giving, pledge=total_pledge))

    # print("arms: ",arms)

    # print('reasb: ',b)
    return render_template('pcf_report.html', title="PCF Report",tmga_colors = chart_colors, cell_performance= cell_performance, total_giving=total_giving, total_pledge=total_pledge, arms_count=arms_count,  member_data=member_data,partner_data=partner_data, monthly_partnership=monthly_partnership)
