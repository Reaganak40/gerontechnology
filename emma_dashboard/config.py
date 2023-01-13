import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DB_NAME = "emma_backend"
    DB_USER = "root"        # ! Fix this.
    DB_PASSWORD = "root"    # ! Fix this.
    TEMPLATE_FOLDER = os.path.join(basedir, 'dashboard//View//templates')