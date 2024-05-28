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

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import HTTPException


class Base(DeclarativeBase):
    def to_dict(self):
        """
        :return: 将模型转换为字典格式
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://qianfuxin:qianfuxin@qianfuxin.com:13306/backend"
)
db.init_app(app)
CORS(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Hello World"


def handle_4xx(exception):
    return jsonify(
        {
            "code": exception.code,
            "msg": exception.name,
            "data": exception.description,
        }
    )


def handle_5xx(exception):
    return {
        "code": 500,
        "msg": str(exception),
        "data": None,
    }


# 将所有的HTTP客户端错误信息（4xx）都以json格式返回
app.register_error_handler(HTTPException, handle_4xx)
# 将所有的HTTP服务端错误信息（5xx）都以json格式返回
app.register_error_handler(Exception, handle_5xx)


@app.get("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return [user.to_dict() for user in users]


@app.post("/users")
def user_create():
    user = User(
        username=request.form["username"],
        email=request.form["email"],
    )
    db.session.add(user)
    db.session.commit()
    return f"{user.id}"


@app.get("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id, description="无用户")
    return user.to_dict()


@app.delete("/user/<int:id>")
def user_delete(id):
    user = db.get_or_404(User, id, description="无用户")
    db.session.delete(user)
    db.session.commit()
    return "yes"


@app.put("/user/<int:id>")
def user_update(id):
    user = db.get_or_404(User, id, description="无用户")
    user.username = request.form["username"]
    user.email = request.form["email"]
    db.session.commit()
    return "yes"


@app.errorhandler(404)
def error404(error):
    return {
        "code": 404,
        "msg": error.description,
        "data": None,
    }
