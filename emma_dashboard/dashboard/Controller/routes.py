#!/usr/bin/python

"""All routes or pages that a user can traverse.
"""

# * Modules
from pandas import DataFrame
from flask import render_template
from flask import Blueprint
from config import Config
from dashboard import db

bp_routes = Blueprint("routes", __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

# ! This Hello World is not permanent
@bp_routes.route("/")
def hello_world():
    user_table : DataFrame = db.get_users()
    return render_template("index.html", title="Emma Dashboard", user_t=user_table)