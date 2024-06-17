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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from werkzeug.exceptions import HTTPException

from models import db
from routers import user

app = Flask(__name__)
load_dotenv(".env")
"""
SQLALCHEMY_DATABASE_URI = ""
REDIS_URL = ""
MONGO_URI= ""
"""
app.config.from_mapping(os.environ)
db.init_app(app)
CORS(app)
redis_client = FlaskRedis(app)
mongo_client = PyMongo(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per minute", "10 per second"],
    storage_uri="memory://",
    strategy="fixed-window"
)
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


@app.route("/")
def index():
    # 通过这种方式 快速返回
    abort(408, description="Not Found")
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
    return 'PONG'