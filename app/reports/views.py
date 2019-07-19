from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask import request
from flask import jsonify
from sqlalchemy import or_
from sqlalchemy import text

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
