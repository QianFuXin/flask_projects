# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   
   Author :       FXQ
   date：          2024/5/26 15:24
-------------------------------------------------
"""
import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from models import db
from routers import user

app = Flask(__name__)
load_dotenv(".env")
app.config.from_mapping(os.environ)
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

# 注册蓝本
app.register_blueprint(user.app)


# 处理异常的返回信息
def handle_4xx(exception):
    return jsonify(
        {
            "code": exception.code,
            "msg": exception.description,
            "data": [],
        }
    )


def handle_5xx(exception):
    return {
        "code": 500,
        "msg": str(exception),
        "data": None,
    }


app.register_error_handler(HTTPException, handle_4xx)
app.register_error_handler(Exception, handle_5xx)


@app.route("/")
def index():
    # 通过这种方式 快速返回
    abort(408, description="Not Found")
    return "Hello World"
