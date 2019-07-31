# app/admin/__init__.py

from flask import Blueprint

staff_mgmt = Blueprint('staff_mgmt', __name__)

from . import views
