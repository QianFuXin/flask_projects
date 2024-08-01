# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   提供音乐列表接口
   Author :       FXQ
   date：          2024/5/26 15:24
-------------------------------------------------
"""

import os
import random

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# 定义音乐文件夹路径
MUSIC_FOLDER = os.path.join(os.getcwd(), "static")
app.config['MUSIC_FOLDER'] = MUSIC_FOLDER


@app.route('/api/music', methods=['GET'])
def get_music_list():
    music_files = os.listdir(app.config['MUSIC_FOLDER'])
    if len(music_files) > 10:
        random.sample(music_files, 10)
    data = [{"title": os.path.splitext(mf)[0], "file": f"{request.host_url}{mf}/{mf}", "howl": None} for mf in
            music_files]
    return jsonify(data)
