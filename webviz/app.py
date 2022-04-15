# -*-coding:utf-8-*-

import os
from flask import Flask
from app.manager.ros_manager import RosManager

app = Flask(__name__, static_folder="static", template_folder='templates')

from app.views import showlist, databoard

app.register_blueprint(showlist.bp)
app.register_blueprint(databoard.bp)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    RosManager().loop_end()