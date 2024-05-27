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

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"
