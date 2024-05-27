# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   使用flask+schedule实现动态任务调度
   Author :       FXQ
   date：          2024/5/26 15:24
-------------------------------------------------
"""

import threading
import time

import schedule
from flask import Flask, request, jsonify

app = Flask(__name__)


def initialize():
    def monitor():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=monitor, name="schedule_monitor", daemon=True).start()


with app.app_context():
    initialize()


# 所有的任务都要按照这种命名格式 scheduled_开头，内外函数名一致，具体的函数和调度时间在内函数中定义
# 如果函数过多，可以考虑将函数放在单独的文件中，然后在这里导入
def scheduled_print():
    def inner_scheduled_print():
        print("I'm working...")

    schedule.every(3).seconds.do(inner_scheduled_print)


@app.route("/activate")
def activate():
    active_jobs = [str(i) for i in schedule.get_jobs()]
    return jsonify(active_jobs)


@app.route("/deactivate")
def deactivate():
    active_jobs = [str(i).split("do=")[1].split(",")[0] for i in schedule.get_jobs()]
    all_jobs_list = [
        i
        for i in globals()
        if i.startswith("scheduled_") and callable(globals().get(i))
    ]
    inactive_jobs = [job for job in all_jobs_list if job not in active_jobs]
    return jsonify(inactive_jobs)


@app.route("/")
def all_jobs():
    all_jobs_list = [
        i
        for i in globals()
        if i.startswith("scheduled_") and callable(globals().get(i))
    ]
    return jsonify(all_jobs_list)


@app.route("/start")
def start():
    name = request.args.get("name")
    if name and callable(globals().get(name)):
        globals().get(name)()
        return jsonify({"message": "任务开启成功"})
    return jsonify({"message": "任务开启失败，检查name参数"}), 400


@app.route("/stop")
def stop():
    name = request.args.get("name")
    if name and callable(globals().get(name)):
        for job in schedule.get_jobs():
            if name in str(job.job_func):
                schedule.cancel_job(job)
        return jsonify({"message": "任务停止成功"})
    return jsonify({"message": "任务停止失败，检查name参数"}), 400
