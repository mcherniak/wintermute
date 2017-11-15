from flask import Flask
from flask_bootstrap import Bootstrap

BOOTSTRAP = Bootstrap()


APP = Flask(__name__)
BOOTSTRAP.init_app(APP)

import wintermute.views
