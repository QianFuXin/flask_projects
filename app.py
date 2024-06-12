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

import flask_admin as admin
from dotenv import load_dotenv
from flask import Flask
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
"""
默认的环境变量
SECRET_KEY = ""
SQLALCHEMY_DATABASE_URI = ""
FLASK_ADMIN_SWATCH = 'flatly'
"""
load_dotenv(".env")
app.config.from_mapping(os.environ)
db = SQLAlchemy()
babel = Babel()
admin = admin.Admin(template_mode="bootstrap4")
db.init_app(app)
babel.init_app(app)
admin.init_app(app)


@babel.localeselector
def get_locale():
    return "zh_CN"


class BaseModel(db.Model):
    """
    这是一个基本模型，包含了一些必备的列，和常用的方法
    默认返回未删除的数据，删除的时候设置is_deleted为True，自己使用原生方法请遵守这些规则
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Integer)
    created_by = db.Column(db.String(30))
    deleted_at = db.Column(db.Integer)
    deleted_by = db.Column(db.String(30))
    updated_at = db.Column(db.Integer)
    updated_by = db.Column(db.String(30))
    is_deleted = db.Column(db.Boolean, default=False, index=True)


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    def __unicode__(self):
        return self.name


class CustomView(ModelView):
    form_base_class = SecureForm


class UserAdmin(CustomView):
    column_searchable_list = ("username",)
    column_filters = ("username", "email")
    can_export = True
    export_types = ["csv", "xlsx"]


@app.route("/")
def index():
    return redirect("/admin")


admin.add_view(UserAdmin(User, db.session, category="数据"))
