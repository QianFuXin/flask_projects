# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   上传shell文件，然后执行shell，格式如下
    username:password@ip:port
    cd /tmp
    ls -l
   Author :       FXQ
   date：          2024/5/26 15:24
-------------------------------------------------
"""

import paramiko
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["POST"])
def execute_command():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"})
    content = file.read().decode()
    lines = content.split("\n")
    if len(lines) < 2:
        return jsonify({"error": "File must contain at least two lines"})

    connection_info = lines[0].strip()
    command = "\n".join(lines[1:])
    if "\r" in command:
        command = command.replace("\r", "")

    result = execute_remote_command(connection_info, command)
    return jsonify(result)


def execute_remote_command(connection_info, command):
    result = {"output": None, "error": None}

    try:
        username_password, host_port = connection_info.split("@")
        username, password = username_password.split(":")
        host, port = host_port.split(":")

        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, int(port), username, password)
            print(command)
            # command="ls"
            _, stdout, stderr = client.exec_command(command)

            result["output"] = stdout.read().decode()
            result["error"] = stderr.read().decode()

    except Exception as e:
        result["error"] = str(e)

    return result
