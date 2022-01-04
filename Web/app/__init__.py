# -*- coding:utf-8 -*-
from flask import Flask
from .config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# 数据库
from . import database
database.init_app(app)

from app.views import client_list
app.register_blueprint(client_list.bp)