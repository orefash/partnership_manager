from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home

from data_helper import get_top_partners, get_total_monthly_partnership, get_partnership_by_arms, get_partnership_by_pcfs


@home.route('/dashboard')
@login_required
def show_dashboard():
    """
    Render the homepage template on the / route
    """
    top_partners = get_top_partners()
    monthly_givings = get_total_monthly_partnership()
    monthly_givings_arms, pie_arms_colors = get_partnership_by_arms()
    total_givings_pcf, pie_pcf_colors = get_partnership_by_pcfs()

    return render_template('dashboard.html', title="Dashboard", tp = top_partners, tmg = monthly_givings, tmga = monthly_givings_arms, tmga_colors = pie_arms_colors, tgp = total_givings_pcf, ppc= pie_pcf_colors, active=0)

@home.route('/')
def go_home():
    """
    Render the homepage template on the / route
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.show_dashboard'))
    else:
        return redirect(url_for('auth.user_login'))
