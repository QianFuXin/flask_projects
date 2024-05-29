# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     user.py
   Description :  用户路由
   Author :       FXQ
   date：          2024/5/29 15:16
-------------------------------------------------
"""
from flask import Blueprint, request

from models import db, User, Car

app = Blueprint("user", __name__, url_prefix="/user")


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


@app.get("/getUserByCar/<int:id>")
def getUserByCar(id):
    car = db.get_or_404(Car, id, description="无用户")
    return [i.to_dict() for i in car.user]


@app.get("/getCarByUser/<int:id>")
def getCarByUser(id):
    user = db.get_or_404(User, id, description="无用户")
    return user.car.to_dict()
