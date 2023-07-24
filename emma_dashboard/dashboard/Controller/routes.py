#!/usr/bin/python

"""All routes or pages that a user can traverse.
"""

import os

# * Modules
from pandas import DataFrame
from flask import render_template, request, Blueprint, redirect, url_for
from config import Config
from dashboard import db

try:
    from Model.participant import Participant
except:
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parent_dir) 
    from Model.participant import Participant



bp_routes = Blueprint("routes", __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route("/")
def index():
    user_table : DataFrame = db.get_users()
    return render_template("index.html", title="Emma Dashboard", user_t=user_table)

@bp_routes.route("/participant")
def info():
    participant_id = request.args.get('participant_id')

    try:
        p = Participant(participant_id)
    except KeyError as ke:
        print(f"Unexpected KeyError: {ke}")
        return redirect(url_for('routes.index'), code=302)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

    return render_template("participant.html", title="Participant - {}".format(p.name), participant=p)