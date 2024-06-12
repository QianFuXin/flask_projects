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
import hashlib
import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
"""
环境变量
SQLALCHEMY_DATABASE_URI = ""
JWT_SECRET_KEY = "xxx"
"""
load_dotenv(".env")
app.config.from_mapping(os.environ)
db = SQLAlchemy(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
BAD_USERNAME_PASSWORD_MSG = "Bad username or password"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username is None or password is None:
        return jsonify({"msg": BAD_USERNAME_PASSWORD_MSG})
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = db.session.execute(
        db.select(User).where(
            User.username == username, User.password == hashed_password
        )
    ).one_or_none()
    if user is None:
        return jsonify({"msg": BAD_USERNAME_PASSWORD_MSG})
    user = user[0]
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@app.route("/validator")
@jwt_required()
def validator():
    current_user = get_jwt_identity()
    return jsonify(msg=current_user)
