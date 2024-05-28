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

from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
upload_dir = "./uploaded_images"

# Ensure the upload directory exists
os.makedirs(upload_dir, exist_ok=True)


@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图片上传页面</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }
        .upload-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .upload-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .upload-btn:hover {
            background-color: #45a049;
        }
        input[type="file"] {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="upload-container">
        <h2>上传图片</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" id="file-upload" name="file" accept="image/*">
            <button type="submit" class="upload-btn">上传图片</button>
        </form>
    </div>
</body>
</html>
"""
    return render_template_string(html)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "No file provided", 400

    # Calculate SHA-256 hash of the file
    hasher = hashlib.sha256()
    file_content = file.read()
    hasher.update(file_content)
    file.seek(0)  # Move cursor back to beginning of file for later operations

    filename = hasher.hexdigest() + os.path.splitext(file.filename)[1]
    file_path = os.path.join(upload_dir, filename)
    if not os.path.exists(file_path):
        file.save(file_path)
    return_url = f"http://{request.host}/files/{filename}"
    html_template = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>上传成功</title>
<style>
    body {
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0;
    }
    #copyButton {
        padding: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-right: 10px;
    }
    a {
        padding: 10px;
        background-color: #007BFF;
        color: white;
        text-decoration: none;
        border-radius: 5px;
    }
</style>
<script>
    function copyURL() {
        var copyText = document.getElementById("urlField");
        copyText.select();
        document.execCommand("copy");
        alert("Copied the URL: " + copyText.value);
    }
</script>
</head>
<body>
    <div>
        <p>文件上传成功！</p>
        <input type="text" value="{return_url}" id="urlField" readonly style="width:300px;">
        <button id="copyButton" onclick="copyURL()">复制URL</button>
        <a href="{return_url}" target="_blank">访问文件</a>
    </div>
</body>
</html>
"""
    html_template = html_template.replace("{return_url}", return_url)
    return render_template_string(html_template)


@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(upload_dir, filename)
