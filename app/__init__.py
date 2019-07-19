# app/__init__.py

# third-party imports
from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# after existing third-party imports
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

import os

# db variable initialization
db = SQLAlchemy()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# after the db variable initialization
login_manager = LoginManager()

chart_colors = [
    "#f56954", "#00a65a", "#f39c12", "#00c0ef",
    "#3c8dbc", "#FEDCBA", "#FDB45C", "#4169E1",
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
    # app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')


    # app.config['D_FOLDER'] = D_FOLDER
    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.user_login"

    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .reports import reports as reports_blueprint
    app.register_blueprint(reports_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500


    return app



def initialize_pcf_cell():
    from app import models
    from models import Pcf, Cell

    from datetime import date
    today = date.today()
    # print("today ", today)
    t_date = today.strftime("%Y/%m/%d")

    import pandas as pd

    file = 'CG.xlsx'

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', file)

    # Load spreadsheet
    xl = pd.ExcelFile(path)

    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse('Sheet1')

    cells = df1.iloc[:, 0].tolist()
    pcfs = df1.iloc[:, 1].tolist()

    d = {}
    for i in pcfs:
        d[i] = []

    for i in range(len(cells)):
        d[pcfs[i]].append(cells[i])

    # print(d)

    pcf_list = list(d.keys())
    pcf_id = {}

    for pcf in pcf_list:
        pcf_item = Pcf(pcf=pcf, entry_date=t_date)
        db.session.add(pcf_item)
        db.session.flush()
        # print(pcf_item.id)
        pcf_id[pcf] = pcf_item.id

    for pcf in pcf_list:

        pcells = d[pcf]
        # print(pcells)
        for pc in pcells:
            cell_item = Cell(pcf_id=pcf_id[pcf], cell=pc, entry_date=t_date)
            db.session.add(cell_item)

    db.session.commit()



def initialize_roles():
    from app import models
    from models import Staff_Role

    from datetime import date
    today = date.today()
    # print("today ", today)
    t_date = today.strftime("%Y/%m/%d")

    staff_roles = []

    staff_roles.append(Staff_Role(role='Administrator', description='Administrator', entry_date=t_date))
    staff_roles.append(Staff_Role(role='Staff', description='Staff', entry_date=t_date))

    for role in staff_roles:
        db.session.add(role)
    db.session.commit()

def initialize_group_church():
    from app import models
    from models import Group, Church

    from datetime import date
    today = date.today()
    # print("today ", today)
    t_date = today.strftime("%Y/%m/%d")

    group = Group(group='ISLAND 2 GROUP', entry_date=t_date)
    db.session.add(group)
    db.session.flush()

    church = Church(group_id=group.id, church='CE IKOYI', entry_date=t_date)
    db.session.add(church)
    db.session.commit()

def initialize_partner_arms():
    from app import models
    from models import PartnershipArm

    from datetime import date
    today = date.today()
    # print("today ", today)
    t_date = today.strftime("%Y/%m/%d")

    file = 'arms.csv'

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', file)

    import csv

    p_arms = []
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            p_arms = row

    for arm in p_arms:
        p_arm = PartnershipArm(partnership_arm=arm, entry_date=t_date)
        db.session.add(p_arm)
    db.session.commit()




def initialize_dbs():
    #init group n church
    initialize_group_church()

    #init roles
    initialize_roles()

    #init pcf cells
    initialize_pcf_cell()

    #init partner arm
    initialize_partner_arms()
