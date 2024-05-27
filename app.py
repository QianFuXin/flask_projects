# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   使用flask实现的词云生成服务
   Author :       FXQ
   date：          2024/5/26 15:24
-------------------------------------------------
"""
from collections import Counter
from io import BytesIO

import jieba
from flask import Flask, request, send_file, jsonify
from wordcloud import WordCloud

app = Flask(__name__)

stopwords = open(r"stopwords.txt", "r", encoding="utf-8").read()
font_path = r"STKAITI.TTF"


def condition(s):
    if s.strip() and s not in stopwords:
        return True
    return False


def generate_wordcloud(word_list):
    word_frequency = dict(Counter(word_list))
    sorted_word_frequency = dict(
        sorted(word_frequency.items(), key=lambda item: item[1], reverse=True)
    )

    wordcloud = WordCloud(
        width=1440,
        height=900,
        background_color="white",
        random_state=42,
        font_path=font_path,
    ).generate_from_frequencies(sorted_word_frequency)
    image = wordcloud.to_image()
    return image


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]

    if file:
        content = file.read().decode("utf-8")
        seg_list = jieba.cut_for_search(content)
        if "user_dict" in request.files:
            user_dict = request.files["user_dict"]
            need_to_remove_later = user_dict.read().decode("utf-8").splitlines()
            user_dict.seek(0)
            jieba.load_userdict(user_dict)
        word_list = [i for i in seg_list if condition(i)]
        if "user_stopwords" in request.files:
            user_stopwords = (
                request.files["user_stopwords"].read().decode("utf-8").splitlines()
            )
            word_list = [i for i in word_list if i not in user_stopwords]
        image = generate_wordcloud(word_list)

        img_io = BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)
        # 删除本次请求的用户词典
        if "user_dict" in request.files:
            for i in need_to_remove_later:
                jieba.del_word(i)
        return send_file(
            img_io,
            mimetype="image/png",
            as_attachment=True,
            download_name="wordcloud.png",
        )
