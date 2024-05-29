# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     models.py
   Description :   存放orm相关
   Author :       FXQ
   date：          2024/5/29 15:01
-------------------------------------------------
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, backref


class Base(DeclarativeBase):
    def to_dict(self):
        """
        :return: 将模型转换为字典格式
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.car_id"))
    car: Mapped["Car"] = relationship("Car", backref=backref("user"))


class Car(db.Model):
    car_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
