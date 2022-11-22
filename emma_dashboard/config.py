import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DB_NAME = "sample_users.accdb"
    DB_FOLDER = os.path.join(basedir, 'data//sample db')
    TEMPLATE_FOLDER = os.path.join(basedir, 'dashboard//View//templates')