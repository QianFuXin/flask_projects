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
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# 定义音乐文件夹路径
MUSIC_FOLDER = os.path.join(os.getcwd(), "static")
app.config['MUSIC_FOLDER'] = MUSIC_FOLDER

# 全局缓存字典
music_files_cache = {
    'data': None,
    'timestamp': None
}

# 缓存超时时间（秒）
CACHE_TIMEOUT = 60


# 获取指定目录下的所有文件
def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list


@app.route('/api/music', methods=['GET'])
def get_music_list():
    global music_files_cache
    current_time = time.time()
    # 检查缓存是否存在且未过期
    if music_files_cache['data'] is not None and (current_time - music_files_cache['timestamp']) < CACHE_TIMEOUT:
        music_files = music_files_cache['data']
    else:
        # 重新生成数据
        music_files = get_all_files(app.config['MUSIC_FOLDER'])
        # 更新缓存
        music_files_cache['data'] = music_files
        music_files_cache['timestamp'] = current_time
    if len(music_files) > 5:
        music_files = random.sample(music_files, 5)
    data = [{"title": os.path.splitext(os.path.basename(mf))[0], "file": f"{request.host_url}static/{mf}", "howl": None}
            for mf in
            music_files]
    return jsonify(data)
