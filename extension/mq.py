# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mq.py
   Description :  rabbitMQ消息队列的生产者扩展
   Author :       FXQ
   date：          2024/7/24 14:18
-------------------------------------------------
"""
import pika


class FlaskRaMQ:
    def __init__(self, app=None):
        self._channel = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        mq_host = app.config.get("MQ_HOST", "localhost")
        mq_port = app.config.get("MQ_PORT", 5672)
        mq_user = app.config.get("MQ_USER", "guest")
        mq_pass = app.config.get("MQ_PASS", "guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                mq_host, mq_port, "/", pika.PlainCredentials(mq_user, mq_pass)
            )
        )
        self._channel = connection.channel()

    @property
    def channel(self):
        return self._channel
