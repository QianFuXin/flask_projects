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

import requests
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from werkzeug.exceptions import HTTPException

from extension.email import FlaskQQEmail
from models import db
from routers import user

app = Flask(__name__)
load_dotenv(".env")
"""
SQLALCHEMY_DATABASE_URI = ""
REDIS_URL = ""
MONGO_URI= ""
QQ_EMAIL= ""
QQ_EMAIL_PASSWORD= ""
STRAPI_DOMAIN= ""
"""
app.config.from_mapping(os.environ)
strapi_domain = app.config.get("STRAPI_DOMAIN", "localhost:1337")
db.init_app(app)
CORS(app)
redis_client = FlaskRedis(app)
mongo_client = PyMongo(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per minute", "10 per second"],
    storage_uri="memory://",
    strategy="fixed-window",
)
email_client = FlaskQQEmail(app)
migrate = Migrate(app, db)
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


# 请求前
@app.before_request
def before_request():
    # 使用strapi作为认证中心
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="Unauthorized")
    if token.split(" ")[0] != "Bearer":
        abort(401, description="Unauthorized")
    res = requests.get(
        f"http://{strapi_domain}/api/users/me", headers={"Authorization": token}
    )
    if res.status_code != 200:
        abort(401, description="Unauthorized")
    g.user_id = res.json().get("id")


@app.route("/")
def index():
    # 通过这种方式 快速返回
    abort(408, description="Not Found")
    return "Hello World"


@app.route("/strapi")
def strapi():
    # 获取user_id
    print(g.get("user_id"))
    return "Hello World"


@app.route("/redis")
def redis():
    # 详细接口查看redis-py文档
    return redis_client.get("potato")


@app.route("/mongo")
def mongo():
    # 详细接口查看pymongo文档
    return str(mongo_client.db.testcol.find_one())


@app.route("/slow")
@limiter.limit("1 per day")
def slow():
    return "24"


@app.route("/fast")
def fast():
    return "42"


@app.route("/ping")
@limiter.exempt
def ping():
    return "PONG"


@app.route("/email")
def email():
    to = "Mr_Qian_ives@163.com"
    subject = "Test Email from yagmail"
    contents = [
        "This is the body, and here is just text http://somedomain/image.png",
        "You can find an audio file attached.",
        "1.py",
    ]
    email_client.yag.send(to=to, subject=subject, contents=contents)
    return "ok"
