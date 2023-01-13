#!/usr/bin/python

""" This file contains app configuration and database connection code.
"""

# * Modules
from flask import Flask
from config import Config
from sqlalchemy import create_engine
from .Model.database import Database

def connect_db(config_class = Config):
    connection_str = "mysql://{}:{}@localhost/{}".format(Config.DB_USER, Config.DB_PASSWORD, Config.DB_NAME)
    db_engine = create_engine(connection_str)
    return Database(db_engine)

db : Database = connect_db()

# ==========================================================
# ? Recent Updates: Added blueprints.
# * Update Date:    10/29/2022
# ==========================================================
def create_app(config_class=Config):
    """This creates an instance of the dashboard GUI application. 
    While this is created and running, the user can interact with participant data within the UI.

    Args:
        config_class (Config, optional): Provides macro definitions for Flask, 
        all dependent on local directory files. Defaults to Config (This is fine).

    Returns:
        Flask: An instance of the Flask application which is the GUI.
    """
    app = Flask(__name__)

    # This tells routes where to find html files.
    app.template_folder = config_class.TEMPLATE_FOLDER
    
    # Using blueprints allows use to define routes in different parts
    #  of the application, which also allows us to use the MVC architecture model.
    from dashboard.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)
    return app

