#!/usr/bin/python

"""A GUI for clinicians that showcases participant data from the EMMA app. Coded with Python using Flask.
"""

# * Modules
from dashboard import create_app, db
from dashboard.Model.model import User

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

__author__ = "Reagan Kelley"
__copyright__ = "N/A"
__credits__ = ["Reagan Kelley"]
__license__ = "Apache License"
__version__ = "0.0.1"
__maintainer__ = "Reagan Kelley"
__email__ = "reagan.kelley@wsu.edu"
__status__ = "Development"

# Create dashboard application
app = create_app()

# ==========================================================
# ? Recent Updates: Added Pass.
# * Update Date:    10/29/2022
# ==========================================================
@app.before_first_request
def init_db():
    db.create_all()
 
if __name__ == "__main__":
    app.run()